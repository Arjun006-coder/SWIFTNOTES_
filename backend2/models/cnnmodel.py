import tensorflow as tf
from tensorflow.keras import layers, models

def build_custom_cnn(input_shape=(224, 224, 3)):
    # 1. The main "Backbone" - This extracts the features from the image
    backbone = models.Sequential([
        layers.Input(shape=input_shape),
        layers.Conv2D(32, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),
        layers.Flatten(),
        layers.Dense(128, activation='relu')
    ], name="feature_extractor")

    # We still need a starting point for the data
    inputs = layers.Input(shape=input_shape)
    features = backbone(inputs)

    # 2. The Classification Head (Is it a Formula or Code?)
    # We use a simple Dense layer directly on the features
    class_out = layers.Dense(2, activation='softmax', name='class_output')(features)
    
    # 3. The Bounding Box Head (Where is it?)
    # We use another Dense layer on the same features
    box_out = layers.Dense(4, activation='sigmoid', name='box_output')(features)

    # Combine them into one model
    model = models.Model(inputs=inputs, outputs=[class_out, box_out])
    
    model.compile(
        optimizer='adam', 
        loss={
            'class_output': 'sparse_categorical_crossentropy', 
            'box_output': 'mse'
        }
    )
    return model