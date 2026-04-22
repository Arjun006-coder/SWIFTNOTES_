import torch
import torch.nn as nn
import torch.nn.functional as F

class LSTMSummarizer(nn.Module):
    def __init__(self, vocab_size, embedding_dim=128, latent_dim=256):
        super(LSTMSummarizer, self).__init__()
        self.latent_dim = latent_dim
        
        # Embedding Layer
        self.embedding = nn.Embedding(vocab_size, embedding_dim, padding_idx=0)
        
        # Encoder: Bidirectional LSTM
        self.encoder_lstm = nn.LSTM(embedding_dim, latent_dim, batch_first=True, bidirectional=True)
        
        # Decoder: LSTM (Hidden state size is latent_dim * 2 to match Bi-LSTM output)
        self.decoder_lstm = nn.LSTM(embedding_dim, latent_dim * 2, batch_first=True)
        
        # Attention and Output
        self.fc = nn.Linear(latent_dim * 4, vocab_size) # latent_dim*2 (decoder) + latent_dim*2 (attention)

    def forward(self, source, decoder_input):
        # 1. Encoder
        encoder_outputs, (h_n, c_n) = self.encoder_lstm(self.embedding(source))
        
        # Concatenate forward and backward states for the decoder initial state
        # h_n shape: [2, batch, latent_dim] -> [1, batch, latent_dim*2]
        state_h = torch.cat((h_n[0], h_n[1]), dim=1).unsqueeze(0)
        state_c = torch.cat((c_n[0], c_n[1]), dim=1).unsqueeze(0)
        
        # 2. Decoder
        decoder_outputs, _ = self.decoder_lstm(self.embedding(decoder_input), (state_h, state_c))
        
        # 3. Simple Dot-Product Attention
        # Shape: (batch, seq_len_dec, seq_len_enc)
        attention_scores = torch.bmm(decoder_outputs, encoder_outputs.transpose(1, 2))
        attention_weights = F.softmax(attention_scores, dim=-1)
        context_vector = torch.bmm(attention_weights, encoder_outputs)
        
        # 4. Final Output (Concat context and decoder output)
        combined = torch.cat((decoder_outputs, context_vector), dim=-1)
        logits = self.fc(combined)
        
        return logits