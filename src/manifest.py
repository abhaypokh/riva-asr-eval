import json, soundfile as sf, os


def make_manifest(input_path, output_path, start_index=0, end_index=None):
    parakeet_dir = os.path.join(input_path, "parakeet")
    real_dir = os.path.join(input_path, "real")
    audio_dir = os.path.join(input_path, "audio")
    with open(output_path, "w") as f:
        for filename in sorted(os.listdir(parakeet_dir))[start_index:end_index]:
            if not filename.endswith(".txt"):
                continue
            stem = os.path.splitext(filename)[0]
            with open(os.path.join(real_dir, filename)) as rf:
                text = rf.read().strip()
            audio_path = os.path.join(audio_dir, stem, "final.wav")
            info = sf.info(audio_path)
            duration = info.frames / info.samplerate
            f.write(json.dumps({
                "audio_filepath": os.path.abspath(audio_path),
                "duration": duration,
                "text": text,
            }) + "\n")


if __name__ == "__main__":
    make_manifest("out", "out/train.jsonl", end_index=25)
    make_manifest("out", "out/val.jsonl", start_index=-5)
