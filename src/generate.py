from anonymize import anonymize
from transcript import generate_audio_from_transcript
import os
from tqdm import tqdm
from time import time


def generate(input_dir, output_dir, character_voice_ids, audio_filename="final.wav",
             use_parakeet=True, use_canary=True, use_whisper=True, use_parakeet_finetuned=True):
    transcripts_dir = os.path.join(input_dir, "transcripts")
    audio_dir = os.path.join(output_dir, "audio")
    real_dir = os.path.join(output_dir, "real")
    parakeet_dir = os.path.join(output_dir, "parakeet")
    canary_dir = os.path.join(output_dir, "canary")
    whisper_dir = os.path.join(output_dir, "whisper")
    parakeet_finetuned_dir = os.path.join(output_dir, "parakeet_finetuned")
    os.makedirs(real_dir, exist_ok=True)

    if use_parakeet:
        from parakeet_decode import decode_parakeet
    if use_canary:
        from canary_decode import decode_canary
    if use_whisper:
        from whisper_decode import decode_whisper
    if use_parakeet_finetuned:
        from nemo_decode import decode_nemo

    parakeet_times = []
    canary_times = []
    whisper_times = []
    parakeet_finetuned_times = []
    for filename in tqdm(sorted(os.listdir(transcripts_dir)), desc="Processing transcripts"):
        if filename.endswith(".txt"):
            with open(os.path.join(transcripts_dir, filename)) as f:
                transcript = f.read()

            anonymized_transcript = anonymize(transcript, placeholder="person")
            audio_subdir = os.path.join(audio_dir, os.path.splitext(filename)[0])
            real = generate_audio_from_transcript(anonymized_transcript, character_voice_ids, audio_subdir)
            with open(os.path.join(real_dir, os.path.splitext(filename)[0] + ".txt"), "w") as f:
                f.write(real)
            audio_path = os.path.join(audio_subdir, audio_filename)
            if use_parakeet:
                start_time = time()
                decode_parakeet([audio_path], parakeet_dir)
                parakeet_times.append(time() - start_time)
            if use_canary:
                start_time = time()
                decode_canary([audio_path], canary_dir)
                canary_times.append(time() - start_time)
            if use_whisper:
                start_time = time()
                decode_whisper([audio_path], whisper_dir)
                whisper_times.append(time() - start_time)
            if use_parakeet_finetuned:
                start_time = time()
                decode_nemo([audio_path], parakeet_finetuned_dir)
                parakeet_finetuned_times.append(time() - start_time)

    if use_parakeet:
        print(f"Average Parakeet decoding time: {sum(parakeet_times[1:]) / len(parakeet_times[1:]):.2f} seconds")
    if use_canary:
        print(f"Average Canary decoding time: {sum(canary_times[1:]) / len(canary_times[1:]):.2f} seconds")
    if use_whisper:
        print(f"Average Whisper decoding time: {sum(whisper_times[1:]) / len(whisper_times[1:]):.2f} seconds")
    if use_parakeet_finetuned:
        print(f"Average Parakeet finetuned decoding time: {sum(parakeet_finetuned_times[1:]) / len(parakeet_finetuned_times[1:]):.2f} seconds")


if __name__ == "__main__":
    character_voice_ids = {
        "[CLIENT]": "Matthew",
        "[RECEPTIONIST]": "Joanna",
    }
    generate("data", "out", character_voice_ids, audio_filename="1.wav",
             use_parakeet=False, use_canary=False, use_whisper=False,
             use_parakeet_finetuned=True)
