# dataset_generator.py
import pandas as pd
import random

def generate_synthetic_data(samples=5000):
    topics = ["Artificial Intelligence", "Blockchain", "Cloud Computing", "Web Dev"]
    data = []
    
    for _ in range(samples):
        topic = random.choice(topics)
        # Simulating a transcript
        transcript = f"In this video we talk about {topic}. " * 50 
        # Simulating a summary
        summary = f"A comprehensive guide to {topic}."
        data.append({"transcript": transcript, "summary": summary})
    
    df = pd.DataFrame(data)
    df.to_csv("data/raw_transcripts.csv", index=False)
    print(f"Generated {samples} samples in data/raw_transcripts.csv")

if __name__ == "__main__":
    generate_synthetic_data()