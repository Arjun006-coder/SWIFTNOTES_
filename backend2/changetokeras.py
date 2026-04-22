import tensorflow as tf
# Try loading it. If this fails with the 'mse' error, you MUST retrain.
try:
    model = tf.keras.models.load_model("models/cnn_detector.h5", compile=False)
    # Re-compile with the string names that Keras 3 likes
    model.compile(
        optimizer='adam',
        loss={'class_output': 'sparse_categorical_crossentropy', 'box_output': 'mean_squared_error'}
    )
    model.save("models/cnn_detector.keras")
    print("Success! Model converted without retraining.")
except Exception as e:
    print(f"Conversion failed: {e}. A retrain is required.")