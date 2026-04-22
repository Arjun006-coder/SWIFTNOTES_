import torch
import joblib
import numpy as np
import os
import sys
from tensorflow.keras.preprocessing.sequence import pad_sequences
from models.transformer_engine import get_transformer_summary
from utils.transcript_fetcher import get_clean_transcript
from utils.video_streamer import stream_video
from models.lstm_summarizer import LSTMSummarizer

# Set up device for GPU acceleration
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def get_full_video_summary(full_text, chunk_size=3000):
    """Summarizes large transcripts using a Map-Reduce approach."""
    if len(full_text) < 100:
        return "Transcript too short for global summary."

    chunks = [full_text[i:i+chunk_size] for i in range(0, len(full_text), chunk_size)]
    intermediate_summaries = []
    max_chunks = min(len(chunks), 8)
    
    for i in range(max_chunks): 
        print(f"Processing chunk {i+1}/{max_chunks}...")
        summary = get_transformer_summary(chunks[i])
        intermediate_summaries.append(summary)
    
    final_report = "\n- ".join(intermediate_summaries)
    return f"This video covers the following key points:\n- {final_report}"

def generate_lstm_summary(model, x_tokenizer, text, max_len_text=270, max_len_summ=50):
    """Inference loop for the PyTorch LSTM model."""
    model.eval()
    y_tokenizer = joblib.load('models/y_tokenizer.pkl')
    reverse_y_map = {i: w for w, i in y_tokenizer.word_index.items()}
    
    seq = x_tokenizer.texts_to_sequences([text])
    padded_x = pad_sequences(seq, maxlen=max_len_text, padding='post')
    input_tensor = torch.LongTensor(padded_x).to(device)
    
    decoded_seq = np.zeros((1, max_len_summ))
    decoded_seq[0, 0] = y_tokenizer.word_index.get('sostoken', 1)
    
    result_words = []
    with torch.no_grad():
        for i in range(max_len_summ - 1):
            decoder_input_tensor = torch.LongTensor(decoded_seq).to(device)
            output = model(input_tensor, decoder_input_tensor)
            sampled_token_index = torch.argmax(output[0, i, :]).item()
            sampled_word = reverse_y_map.get(sampled_token_index, '')
            
            if sampled_word == 'eostoken' or sampled_word == '':
                break
            result_words.append(sampled_word)
            
            if i + 1 < max_len_summ:
                decoded_seq[0, i+1] = sampled_token_index

    return ' '.join(result_words).strip()

def run_evaluation():
    URL = "https://www.youtube.com/watch?v=VmbA0pi2cRQ" 
    results_content = [] # List to store all summary outputs

    # 1. Fetch Transcript
    print("\n--- [1/4] FETCHING TRANSCRIPT ---")
    try:
        text = get_clean_transcript(URL)
        results_content.append(f"TRANSCRIPT FETCHED (Length: {len(text)} chars)\n" + "="*30 + "\n")
    except Exception as e:
        print(f"Error: {e}")
        return

    # 2. Transformer Test
    print("\n--- [2/4] TEST: Transformer (BART) Global Summary ---")
    global_summary = get_full_video_summary(text)
    results_content.append("TEST 1: TRANSFORMER (BART) GLOBAL SUMMARY\n" + global_summary + "\n\n")

    # 3. LSTM Test
    print("\n--- [3/4] TEST: Custom PyTorch LSTM Summary ---")
    try:
        vocab_size = 10000 
        lstm_model = LSTMSummarizer(vocab_size).to(device)
        model_path = 'models/lstm_final.pth'
        
        if os.path.exists(model_path):
            lstm_model.load_state_dict(torch.load(model_path, map_location=device, weights_only=True))
            x_tokenizer = joblib.load('models/x_tokenizer.pkl')
            lstm_summary = generate_lstm_summary(lstm_model, x_tokenizer, text[:500])
            results_content.append("TEST 2: CUSTOM PYTORCH LSTM SUMMARY\n" + lstm_summary + "\n\n")
        else:
            results_content.append("TEST 2: LSTM model not found.\n\n")
    except Exception as e:
        results_content.append(f"TEST 2: LSTM Error: {e}\n\n")

    # 4. Save Summaries to TXT
    with open("evaluation_results.txt", "w", encoding="utf-8") as f:
        f.writelines(results_content)
    print("\n✅ Summaries saved to evaluation_results.txt")

    # 5. Vision Tests (Launches the PyQt6 Player)
    print("\n--- [4/4] STARTING VIDEO VISION TESTS ---")
    
    print("\nLaunching Custom CNN Player...")
    try:
        stream_video(URL, mode='cnn')
    except Exception as e:
        print(f"CNN Player Error: {e}")

    print("\nLaunching YOLOv8 Player...")
    try:
        stream_video(URL, mode='yolo')
    except Exception as e:
        print(f"YOLO Player Error: {e}")

if __name__ == "__main__":
    run_evaluation()