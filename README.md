# 🎧 MP3 Chunk Transcriber w/ OpenAI Whisper + FFmpeg

This Python script:
1. Splits a long `.mp3` file into smaller chunks using `ffmpeg`.
2. Sends each chunk to OpenAI’s Whisper API for transcription.
3. Merges the output into a single text file.

---

## 🛠️ Requirements

- Python 3.7+
- [FFmpeg](https://ffmpeg.org/) installed and added to your PATH
- An OpenAI API key with Whisper access

---

## 🔧 Setup

Install dependencies:
```bash
pip install openai
```

Set your OpenAI API key:
```bash
export OPENAI_API_KEY=your_key_here  # On Windows: set OPENAI_API_KEY=your_key_here
```

---

## ▶️ Usage

Update the following variables in `transcribe_mp3_chunks.py`:
- `input_mp3` → path to your `.mp3` file
- `output_dir` → folder to store audio chunks
- `final_output` → output `.txt` file
- `chunk_minutes` → how long each chunk should be

Then run:
```bash
python transcribe_mp3_chunks.py
```

---

## 📂 Output

- Individual `.mp3` chunks saved in `output_dir`
- A combined transcript in `final_output`

---

## ❗ Notes

- This uses OpenAI’s Whisper (`whisper-1`) model.
- Chunks are downsampled to mono, 16kHz, and 64k bitrate for Whisper compatibility.

---
