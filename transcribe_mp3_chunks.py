import os
import math
import subprocess
from openai import OpenAI

# ===== CONFIGURATION =====
API_KEY = os.getenv("OPENAI_API_KEY")  # Set as environment variable
ffmpeg_path = r"ffmpeg"  # Assumes ffmpeg is in system PATH

input_mp3 = r"path_to_your_input_file.mp3"
output_dir = r"output_chunks"
final_output = r"final_transcript.txt"
chunk_minutes = 20
# ==========================

client = OpenAI(api_key=API_KEY)

# Step 1: Split with ffmpeg subprocess
print("🔧 Step 1: Splitting with ffmpeg...")

os.makedirs(output_dir, exist_ok=True)

# Get duration of input file
probe_cmd = [
    ffmpeg_path,
    "-i", input_mp3,
    "-hide_banner"
]
proc = subprocess.Popen(probe_cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
out, err = proc.communicate()
duration_line = [l for l in err.decode().splitlines() if "Duration" in l]
if not duration_line:
    raise Exception("Unable to get duration from ffmpeg output.")
duration_str = duration_line[0].split("Duration:")[1].split(",")[0].strip()
h, m, s = map(float, duration_str.replace(":", " ").split())
total_seconds = int(h * 3600 + m * 60 + s)

# Calculate chunk start times
chunk_seconds = chunk_minutes * 60
num_chunks = math.ceil(total_seconds / chunk_seconds)
chunk_paths = []

for i in range(num_chunks):
    start_time = i * chunk_seconds
    output_file = os.path.join(output_dir, f"chunk_{i+1}.mp3")
    cmd = [
        ffmpeg_path,
        "-ss", str(start_time),
        "-t", str(chunk_seconds),
        "-i", input_mp3,
        "-ac", "1",
        "-ar", "16000",
        "-b:a", "64k",
        output_file,
        "-y"
    ]
    print(f"  ➤ Creating chunk {i+1}/{num_chunks} at {start_time} sec → {output_file}")
    subprocess.run(cmd, check=True)
    chunk_paths.append(output_file)

print(f"✅ Split into {num_chunks} chunks.\n")

# Step 2: Transcribe with OpenAI Whisper API
print("🎙️ Step 2: Transcribing chunks...")

all_transcripts = []

for i, path in enumerate(chunk_paths):
    print(f"\n📤 Transcribing chunk {i+1}/{num_chunks}: {os.path.basename(path)}")
    with open(path, "rb") as f:
        try:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=f,
                response_format="text"
            )
            all_transcripts.append(f"--- Transcript Part {i+1} ---\n{transcript.strip()}\n")
            print(f"✅ Transcribed chunk {i+1}")
        except Exception as e:
            print(f"❌ Error transcribing chunk {i+1}: {e}")

# Step 3: Save final transcript
print("\n📄 Step 3: Saving merged transcript...")

with open(final_output, "w", encoding="utf-8") as f:
    f.writelines(all_transcripts)

print(f"\n✅ All done! Final transcript saved to:\n{final_output}")
