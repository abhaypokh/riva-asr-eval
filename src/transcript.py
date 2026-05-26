import os

from polly import text_to_speech
from stitch import stitch


def generate_audio_from_transcript(transcript, character_voice_ids, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    files = []
    index = 1
    full_text = ""
    for line in transcript.splitlines():
        line = line.strip()
        if not line:
            continue

        colon = line.index(':')
        speaker = line[:colon].strip()
        text = line[colon + 1:].strip()
        full_text += text + " "

        voice_id = character_voice_ids[speaker]
        output_path = os.path.join(output_dir, f"{index}.wav")
        text_to_speech(text, voice_id, output_path)
        files.append(output_path)
        index += 1

    stitch(files, os.path.join(output_dir, "final.wav"))

    return full_text


if __name__ == "__main__":
    with open("data/sample_transcript.txt") as f:
        transcript = f.read()

    character_voice_ids = {
        "[CLIENT]": "Matthew",
        "[RECEPTIONIST]": "Joanna",
    }

    generate_audio_from_transcript(transcript, character_voice_ids, "audio/sample_transcript")
