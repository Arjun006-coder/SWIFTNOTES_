import os
import json
import pandas as pd
from pathlib import Path

def parse_vtssum_repo():
    all_data = []
    base_path = Path("data/VT-SSum")
    print(f"Scanning for JSON files in {base_path.absolute()}...")
    
    json_files = list(base_path.rglob("*.json"))
    
    for json_path in json_files:
        with open(json_path, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
                
                # 1. Reconstruct full transcript from segments
                segments = data.get('segmentation', [])
                full_transcript = " ".join([" ".join(seg) for seg in segments])
                
                # 2. Extract summary sentences from summarization labels
                summarization_dict = data.get('summarization', {})
                summary_sentences = []
                
                for clip_id, clip_info in summarization_dict.items():
                    # Only look at clips marked as part of the summarization task
                    if clip_info.get('is_summarization_sample', False):
                        data_points = clip_info.get('summarization_data', [])
                        for item in data_points:
                            if item.get('label') == 1: # 1 means it belongs in the summary
                                summary_sentences.append(item.get('sent', ''))
                
                full_summary = " ".join(summary_sentences)
                
                if full_transcript and full_summary:
                    all_data.append({
                        'transcript': full_transcript, 
                        'summary': full_summary
                    })
            except Exception as e:
                continue

    if all_data:
        df = pd.DataFrame(all_data)
        output_dir = Path("data")
        output_dir.mkdir(exist_ok=True)
        df.to_csv(output_dir / "raw_transcripts.csv", index=False)
        print(f"✅ Success! Processed {len(all_data)} samples.")
    else:
        print("❌ Failed: Could not extract transcript/summary pairs. Check JSON format.")

if __name__ == "__main__":
    parse_vtssum_repo()