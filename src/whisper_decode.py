import os

import whisper

print("Loading Whisper model...")
model = whisper.load_model("large-v3")
print("Model loaded successfully.")


def decode_whisper(audio_files, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    transcriptions = []
    for audio_file in audio_files:
        result = model.transcribe(audio_file)
        parent_name = os.path.basename(os.path.dirname(audio_file))
        output_path = os.path.join(output_dir, f"{parent_name}.txt")
        with open(output_path, "w") as f:
            f.write(result["text"])
        transcriptions.append(result)
    return transcriptions


if __name__ == "__main__":
    print(decode_whisper(["audio/sample_transcript/final.wav"], "out/sample_whisper.txt"))
