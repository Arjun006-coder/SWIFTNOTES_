import sys
import cv2
import numpy as np
import yt_dlp
from ultralytics import YOLO
import tensorflow as tf
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QSlider, QLabel, QComboBox)
from PyQt6.QtCore import Qt, QTimer, QThread, pyqtSignal
from PyQt6.QtGui import QImage, QPixmap

class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)
    position_signal = pyqtSignal(int)

    def __init__(self, url, mode, parent=None):
        super().__init__(parent)
        self.url = url
        self.mode = mode
        self._run_flag = True
        self.paused = False
        self.speed = 1.0
        self.seek_to_frame = -1
        
        if mode == 'yolo':
            self.model = YOLO("runs/detect/train/weights/best.pt")
        else:
            self.model = tf.keras.models.load_model("models/cnn_detector.keras")

    def run(self):
        ydl_opts = {'format': 'best'}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(self.url, download=False)
            play_url = info['url']

        self.cap = cv2.VideoCapture(play_url)
        self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        while self._run_flag:
            if self.seek_to_frame != -1:
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, self.seek_to_frame)
                self.seek_to_frame = -1

            if not self.paused:
                ret, frame = self.cap.read()
                if ret:
                    current_frame = int(self.cap.get(cv2.CAP_PROP_POS_FRAMES))
                    self.position_signal.emit(current_frame)
                    
                    processed_frame = self.apply_model(frame)
                    self.change_pixmap_signal.emit(processed_frame)
                    
                    # Logic for speed: adjust sleep time
                    base_delay = 30 
                    time_to_sleep = int(base_delay / self.speed)
                    self.msleep(max(1, time_to_sleep))
                else:
                    break
        self.cap.release()

    def apply_model(self, frame):
        display_frame = frame.copy()
        h, w, _ = frame.shape
        if self.mode == 'yolo':
            results = self.model(frame, verbose=False)
            for r in results:
                for box in r.boxes:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    label = f"YOLO: {'Math' if int(box.cls) == 0 else 'Code'}"
                    cv2.rectangle(display_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(display_frame, label, (x1, y1-10), 1, 0.6, (0, 255, 0), 2)
        elif self.mode == 'cnn':
            input_img = cv2.resize(frame, (224, 224)) / 255.0
            input_img = np.expand_dims(input_img, axis=0)
            class_pred, box_pred = self.model.predict(input_img, verbose=0)
            xc, yc, bw, bh = box_pred[0]
            x1, y1 = int((xc - bw/2) * w), int((yc - bh/2) * h)
            x2, y2 = int((xc + bw/2) * w), int((yc + bh/2) * h)
            label = f"CNN: {'Math' if np.argmax(class_pred) == 0 else 'Code'}"
            cv2.rectangle(display_frame, (x1, y1), (x2, y2), (255, 255, 0), 2)
            cv2.putText(display_frame, label, (x1, y1-10), 1, 0.6, (255, 255, 0), 2)
        return display_frame

    def stop(self):
        self._run_flag = False
        self.wait()

class ModernPlayer(QWidget):
    def __init__(self, url, mode):
        super().__init__()
        self.setWindowTitle(f"SwiftNotes Player - {mode.upper()} Mode")
        self.resize(1000, 800)
        self.setStyleSheet("background-color: #121212; color: white;")

        # UI Elements
        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Seek Slider
        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setRange(0, 1000) # Placeholder range
        self.slider.sliderPressed.connect(self.slider_pressed)
        self.slider.sliderReleased.connect(self.slider_released)

        self.play_button = QPushButton("Pause")
        self.play_button.setFixedWidth(80)
        self.play_button.clicked.connect(self.toggle_video)

        self.speed_box = QComboBox()
        self.speed_box.addItems(["0.5x", "1.0x", "1.5x", "2.0x", "5.0x"])
        self.speed_box.setCurrentIndex(1)
        self.speed_box.currentTextChanged.connect(self.change_speed)

        # Layout
        controls = QHBoxLayout()
        controls.addWidget(self.play_button)
        controls.addWidget(self.slider)
        controls.addWidget(QLabel("Speed:"))
        controls.addWidget(self.speed_box)

        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        layout.addLayout(controls)
        self.setLayout(layout)

        # Thread Setup
        self.is_sliding = False
        self.thread = VideoThread(url, mode)
        self.thread.change_pixmap_signal.connect(self.update_image)
        self.thread.position_signal.connect(self.update_slider)
        self.thread.start()

    def slider_pressed(self): self.is_sliding = True
    
    def slider_released(self):
        # Seek to frame
        if self.thread.total_frames > 0:
            target_frame = int((self.slider.value() / 1000) * self.thread.total_frames)
            self.thread.seek_to_frame = target_frame
        self.is_sliding = False

    def update_slider(self, current_frame):
        if not self.is_sliding and self.thread.total_frames > 0:
            pos = int((current_frame / self.thread.total_frames) * 1000)
            self.slider.setValue(pos)

    def toggle_video(self):
        self.thread.paused = not self.thread.paused
        self.play_button.setText("Play" if self.thread.paused else "Pause")

    def change_speed(self, speed_text):
        val = float(speed_text.replace('x', ''))
        self.thread.speed = val

    def update_image(self, cv_img):
        qt_img = self.convert_cv_qt(cv_img)
        self.image_label.setPixmap(qt_img)

    def convert_cv_qt(self, cv_img):
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        q_img = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
        return QPixmap.fromImage(q_img).scaled(960, 540, Qt.AspectRatioMode.KeepAspectRatio)

    def closeEvent(self, event):
        self.thread.stop()
        event.accept()

def stream_video(url, mode='yolo'):
    app = QApplication.instance() or QApplication(sys.argv)
    player = ModernPlayer(url, mode)
    player.show()
    app.exec()