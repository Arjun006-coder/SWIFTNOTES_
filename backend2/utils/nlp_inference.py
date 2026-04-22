import numpy as np
from tensorflow.keras.preprocessing.sequence import pad_sequences
import joblib # Recommended: Save your tokenizer during training using joblib

def generate_lstm_summary(model, tokenizer, text, max_len=100):
    # 1. Tokenize and Pad the input transcript
    sequence = tokenizer.texts_to_sequences([text])
    padded = pad_sequences(sequence, maxlen=max_len, padding='post')
    
    # 2. Start with the 'start' token for the decoder
    # Note: In a production seq2seq, you'd loop through word by word.
    # For this project, we'll do a simplified greedy prediction.
    prediction = model.predict([padded, np.zeros((1, 20))], verbose=0)
    
    # 3. Convert probabilities to word indices
    target_seq = np.argmax(prediction, axis=-1)[0]
    
    # 4. Map indices back to words
    reverse_word_map = {index: word for word, index in tokenizer.word_index.items()}
    summary = ' '.join([reverse_word_map.get(i, '') for i in target_seq if i > 0])
    
    return summary