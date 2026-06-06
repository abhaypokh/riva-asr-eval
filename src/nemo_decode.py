import os

import nemo.collections.asr as nemo_asr

nemo_file = "out/parakeet_finetuned.nemo"
print(f"Loading NeMo model from {nemo_file}...")
model = nemo_asr.models.ASRModel.restore_from(nemo_file)
print("Model loaded successfully.")


def decode_nemo(audio_files, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    transcriptions = model.transcribe(audio_files)
    for audio_file, transcription in zip(audio_files, transcriptions):
        parent_name = os.path.basename(os.path.dirname(audio_file))
        output_path = os.path.join(output_dir, f"{parent_name}.txt")
        with open(output_path, "w") as f:
            f.write(transcription.text)
    return transcriptions


if __name__ == "__main__":
    print(decode_nemo(["out/audio/29/final.wav"], "out/sample_nemo"))
