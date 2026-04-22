import os
import cv2
import numpy as np
import tensorflow as tf
from models.cnnmodel import build_custom_cnn

def load_dataset(dataset_path, split='train', img_size=(224, 224)):
    images = []
    labels = []
    bboxes = []
    
    img_dir = os.path.join(dataset_path, split, 'images')
    lbl_dir = os.path.join(dataset_path, split, 'labels')
    
    for filename in os.listdir(img_dir):
        # Load image
        img_path = os.path.join(img_dir, filename)
        image = cv2.imread(img_path)
        image = cv2.resize(image, img_size) / 255.0
        
        # Load first label from txt (simplified for this CNN)
        lbl_path = os.path.join(lbl_dir, filename.replace('.jpg', '.txt').replace('.png', '.txt'))
        if os.path.exists(lbl_path):
            with open(lbl_path, 'r') as f:
                line = f.readline().split()
                if line:
                    images.append(image)
                    labels.append(int(line[0]))
                    bboxes.append([float(x) for x in line[1:]]) # [x_center, y_center, w, h]

    return np.array(images), np.array(labels), np.array(bboxes)

# Load data
X_train, y_class, y_box = load_dataset('merged_dataset', 'train')

# Build and Train
model = build_custom_cnn()
print("Training Custom CNN...")
model.fit(X_train, {'class_output': y_class, 'box_output': y_box}, epochs=20, batch_size=32)
model.save('models/cnn_detector.h5')