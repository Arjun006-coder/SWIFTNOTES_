# models/transformer_engine.py
from transformers import pipeline

def get_transformer_summary(text):
    # Using BART-Large-CNN (optimized for summarization)
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    summary = summarizer(text, max_length=200, min_length=60, do_sample=False)
    return summary[0]['summary_text']