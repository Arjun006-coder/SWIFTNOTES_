import os
import torch
import torch.nn as nn
import torch.optim as optim
import pandas as pd
import numpy as np
from torch.utils.data import DataLoader, TensorDataset
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import joblib
from models.lstm_summarizer import LSTMSummarizer

# Device Configuration
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"🚀 Training on: {device}")

# 1. Hyperparameters
vocab_size = 10000
max_len_text = 270
max_len_summ = 50
batch_size = 64
epochs = 30
learning_rate = 0.001

# 2. Load and Preprocess Data
df = pd.read_csv('data/raw_transcripts.csv').dropna()
df['summary'] = df['summary'].apply(lambda x: f'sostoken {x} eostoken')

# Tokenization (Keeping Keras Tokenizer as it's great for preprocessing)
x_tokenizer = Tokenizer(num_words=vocab_size, oov_token="<OOV>")
x_tokenizer.fit_on_texts(df['transcript'])
x_padded = pad_sequences(x_tokenizer.texts_to_sequences(df['transcript']), maxlen=max_len_text, padding='post')

y_tokenizer = Tokenizer(num_words=vocab_size, oov_token="<OOV>")
y_tokenizer.fit_on_texts(df['summary'])
y_padded = pad_sequences(y_tokenizer.texts_to_sequences(df['summary']), maxlen=max_len_summ, padding='post')

# Teacher Forcing Split
decoder_input_data = torch.LongTensor(y_padded[:, :-1])
decoder_target_data = torch.LongTensor(y_padded[:, 1:])
encoder_input_data = torch.LongTensor(x_padded)

# Create DataLoader
dataset = TensorDataset(encoder_input_data, decoder_input_data, decoder_target_data)
train_loader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

# 3. Initialize Model, Optimizer, and Loss
model = LSTMSummarizer(vocab_size).to(device)
optimizer = optim.Adam(model.parameters(), lr=learning_rate)
criterion = nn.CrossEntropyLoss(ignore_index=0) # Ignore padding in loss

# 4. Training Loop
print(f"Starting Training on {len(df)} samples...")
for epoch in range(epochs):
    model.train()
    total_loss = 0
    
    for batch_idx, (src, dec_in, target) in enumerate(train_loader):
        src, dec_in, target = src.to(device), dec_in.to(device), target.to(device)
        
        optimizer.zero_grad()
        output = model(src, dec_in) # [batch, seq_len, vocab_size]
        
        # Reshape for CrossEntropyLoss
        loss = criterion(output.view(-1, vocab_size), target.view(-1))
        
        loss.backward()
        optimizer.step()
        
        total_loss += loss.item()
        
    print(f"Epoch [{epoch+1}/{epochs}] - Loss: {total_loss/len(train_loader):.4f}")

# 5. Save Everything
if not os.path.exists('models'): os.makedirs('models')
torch.save(model.state_dict(), 'models/lstm_final.pth')
joblib.dump(x_tokenizer, 'models/x_tokenizer.pkl')
joblib.dump(y_tokenizer, 'models/y_tokenizer.pkl')
print("✅ Training Complete. Model and Tokenizers saved.")