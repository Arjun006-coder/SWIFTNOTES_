# backend2 (Legacy Experimental Backend)

This folder contains early SwiftNotes backend experiments that were built **before** the current Gemini-key-based backend flow in `SwiftNotes2.0Backend`.

Status:
- Legacy/prototype only
- Not used by the current production path
- Kept for reference and research history

Why we switched:
- Experiments here produced inconsistent quality, especially in summary quality.
- `evaluation_results.txt` shows repetitive/noisy transformer output and weak custom LSTM output.
- Because results were not good enough for stable product behavior, the project moved to the Gemini-based pipeline in `SwiftNotes2.0Backend`.

## Folder Intent

`backend2` combines NLP and computer vision experiments:
- Transcript fetching/cleaning from YouTube
- Text summarization tests (BART + custom PyTorch LSTM)
- Formula/code detection experiments (custom CNN + YOLO)
- Dataset preparation and training utilities

## Python Files (Root)

- `main.py`
  - Orchestrates evaluation flow for one YouTube URL.
  - Fetches transcript (`utils/transcript_fetcher.py`), generates map-reduce style BART summaries (`models/transformer_engine.py`), tries custom LSTM summary (`models/lstm_summarizer.py`), writes `evaluation_results.txt`, then launches CV player tests (`utils/video_streamer.py`).
- `train_summarizers.py`
  - Trains custom PyTorch seq2seq + attention LSTM summarizer using `data/raw_transcripts.csv`.
  - Saves `models/lstm_final.pth`, `models/x_tokenizer.pkl`, `models/y_tokenizer.pkl`.
- `train_cnn.py`
  - Loads YOLO-style labeled image data from `merged_dataset/<split>/{images,labels}`.
  - Trains a custom Keras multi-head model (classification + bounding box regression) and saves `models/cnn_detector.h5`.
- `prepareds.py`
  - Parses `data/VT-SSum/**/*.json` and reconstructs transcript-summary pairs.
  - Exports `data/raw_transcripts.csv`.
- `data_generator.py`
  - Generates synthetic transcript-summary pairs into `data/raw_transcripts.csv` (quick bootstrap data).
- `changetokeras.py`
  - Tries converting `models/cnn_detector.h5` to Keras v3-compatible `.keras` format.
- `x.py`
  - Merges two object-detection datasets (`Mathset`, `codeset`) into `merged_dataset`, remapping class IDs for code samples.

## Python Files (`models/`)

- `models/lstm_summarizer.py`
  - Custom PyTorch encoder-decoder model:
  - Bidirectional LSTM encoder
  - LSTM decoder
  - Dot-product attention
  - Linear projection to vocabulary logits
- `models/transformer_engine.py`
  - Hugging Face summarization pipeline wrapper using `facebook/bart-large-cnn`.
- `models/cnnmodel.py`
  - Custom Keras CNN backbone with:
  - `class_output` head (Math vs Code classification)
  - `box_output` head (bounding box regression)

## Python Files (`utils/`)

- `utils/transcript_fetcher.py`
  - Pulls English auto subtitles via `yt_dlp`, cleans VTT artifacts/timestamps/repetitions, returns cleaned transcript text.
- `utils/nlp_inference.py`
  - Simplified tokenizer/model inference helper for LSTM-style summary generation.
  - Legacy utility; not the main flow used in `main.py`.
- `utils/video_streamer.py`
  - PyQt6-based desktop player with OpenCV rendering.
  - Supports YOLO mode (`runs/detect/train/weights/best.pt`) and custom CNN mode (`models/cnn_detector.keras`) with bounding box overlays.

## Notable Artifacts

- `evaluation_results.txt` - saved test outputs from summarization evaluation.
- `models/` - trained/converted model artifacts (`.pth`, `.h5`, `.keras`, tokenizers).
- `runs/detect/` - YOLO training artifacts and metrics.
- `data/VT-SSum`, `merged_dataset/` - raw and prepared experiment datasets.

## Notes

- This folder is preserved for documentation and experimentation history.
- For current development and integrations, use `SwiftNotes2.0Backend` and `SwiftNotes2.0Web`.
