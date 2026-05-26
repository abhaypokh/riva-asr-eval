from anonymize import anonymize
from transcript import generate_audio_from_transcript
from parakeet_decode import decode_parakeet
from whisper_decode import decode_whisper
import os
from tqdm import tqdm
from time import time


def generate(input_dir, output_dir, character_voice_ids):
    transcripts_dir = os.path.join(input_dir, "transcripts")
    audio_dir = os.path.join(output_dir, "audio")
    real_dir = os.path.join(output_dir, "real")
    parakeet_dir = os.path.join(output_dir, "parakeet")
    whisper_dir = os.path.join(output_dir, "whisper")
    os.makedirs(real_dir, exist_ok=True)
    parakeet_times = []
    whisper_times = []
    for filename in tqdm(os.listdir(transcripts_dir), desc="Processing transcripts"):
        if filename.endswith(".txt"):
            with open(os.path.join(transcripts_dir, filename)) as f:
                transcript = f.read()

            anonymized_transcript = anonymize(transcript, placeholder="person")
            audio_subdir = os.path.join(audio_dir, os.path.splitext(filename)[0])
            real = generate_audio_from_transcript(anonymized_transcript, character_voice_ids, audio_subdir)
            with open(os.path.join(real_dir, os.path.splitext(filename)[0] + ".txt"), "w") as f:
                f.write(real)
            start_time = time()
            decode_parakeet([os.path.join(audio_subdir, "final.wav")], parakeet_dir)
            parakeet_time = time() - start_time
            start_time = time()
            decode_whisper([os.path.join(audio_subdir, "final.wav")], whisper_dir)
            whisper_time = time() - start_time
            parakeet_times.append(parakeet_time)
            whisper_times.append(whisper_time)

    print(f"Average Parakeet decoding time: {sum(parakeet_times[1:]) / len(parakeet_times[1:]):.2f} seconds")
    print(f"Average Whisper decoding time: {sum(whisper_times[1:]) / len(whisper_times[1:]):.2f} seconds")
        
    
if __name__ == "__main__":
    character_voice_ids = {
        "[CLIENT]": "Matthew",
        "[RECEPTIONIST]": "Joanna",
    }
    generate("data", "out", character_voice_ids)