from jiwer import wer
import os

from error_rate import get_keywords, get_error_rate


def evaluate_transcriptions(reference_file, predicted_file):
    with open(reference_file, "r") as f:
        reference = f.read().strip()
    with open(predicted_file, "r") as f:
        predicted = f.read().strip()

    error_rate = wer(reference, predicted)
    return error_rate


if __name__ == "__main__":
    keywords = get_keywords("data/keywords.txt")

    parakeet_wers = []
    whisper_wers = []
    parakeet_keyword_errors = []
    whisper_keyword_errors = []

    for filename in os.listdir("out/real"):
        if filename.endswith(".txt"):
            real_file = os.path.join("out/real", filename)
            parakeet_file = os.path.join("out/parakeet", filename)
            whisper_file = os.path.join("out/whisper", filename)
            parakeet_wer = evaluate_transcriptions(real_file, parakeet_file)
            whisper_wer = evaluate_transcriptions(real_file, whisper_file)
            parakeet_wers.append(parakeet_wer)
            whisper_wers.append(whisper_wer)
            parakeet_keyword_errors.append(get_error_rate(real_file, parakeet_file, keywords))
            whisper_keyword_errors.append(get_error_rate(real_file, whisper_file, keywords))

    print(f"Average Parakeet WER: {sum(parakeet_wers) / len(parakeet_wers):.2%}")
    print(f"Average Whisper WER: {sum(whisper_wers) / len(whisper_wers):.2%}")
    print(f"Average Parakeet keyword error rate: {sum(parakeet_keyword_errors) / len(parakeet_keyword_errors):.2%}")
    print(f"Average Whisper keyword error rate: {sum(whisper_keyword_errors) / len(whisper_keyword_errors):.2%}")
            
