import boto3
import wave
from contextlib import closing

print("Loading AWS Polly client...")
polly = boto3.client('polly')
print("AWS Polly client loaded successfully.")


def text_to_speech(text, voice_id, output_path="output.wav"):
    response = polly.synthesize_speech(
        Text=text,
        OutputFormat='pcm',
        VoiceId=voice_id
    )

    if 'AudioStream' in response:
        with closing(response['AudioStream']) as stream:
            with wave.open(output_path, 'wb') as wav_file:
                wav_file.setparams((1, 2, 16000, 0, 'NONE', 'NONE'))
                wav_file.writeframes(stream.read())

        print(f"File saved successfully as {output_path}")
