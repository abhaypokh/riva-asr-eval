import os

import nemo.collections.asr as nemo_asr

print("Loading Canary model...")
model = nemo_asr.models.ASRModel.from_pretrained("nvidia/canary-1b-v2")
print("Model loaded successfully.")


def decode_canary(audio_files, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    transcriptions = model.transcribe(audio_files)
    for audio_file, transcription in zip(audio_files, transcriptions):
        parent_name = os.path.basename(os.path.dirname(audio_file))
        output_path = os.path.join(output_dir, f"{parent_name}.txt")
        with open(output_path, "w") as f:
            f.write(transcription.text)
    return transcriptions


if __name__ == "__main__":
    print(decode_canary(["audio/sample_transcript/final.wav"], "out/sample_canary.txt"))
