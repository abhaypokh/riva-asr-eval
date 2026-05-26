from anonymize import anonymize
from transcript import generate_audio_from_transcript
from parakeet_decode import decode_parakeet
from whisper_decode import decode_whisper
import os
from tqdm import tqdm


def generate(input_dir, output_dir, character_voice_ids):
    transcripts_dir = os.path.join(input_dir, "transcripts")
    audio_dir = os.path.join(input_dir, "audio")
    parakeet_dir = os.path.join(output_dir, "parakeet")
    whisper_dir = os.path.join(output_dir, "whisper")
    for filename in tqdm(os.listdir(transcripts_dir), desc="Processing transcripts"):
        if filename.endswith(".txt"):
            with open(os.path.join(transcripts_dir, filename)) as f:
                transcript = f.read()

            anonymized_transcript = anonymize(transcript)
            audio_subdir = os.path.join(audio_dir, os.path.splitext(filename)[0])
            generate_audio_from_transcript(anonymized_transcript, character_voice_ids, audio_subdir)
            decode_parakeet([os.path.join(audio_subdir, "final.wav")], parakeet_dir)
            decode_whisper([os.path.join(audio_subdir, "final.wav")], whisper_dir)
        
    
if __name__ == "__main__":
    character_voice_ids = {
        "[CLIENT]": "Matthew",
        "[RECEPTIONIST]": "Joanna",
    }
    generate("data", "out", character_voice_ids)