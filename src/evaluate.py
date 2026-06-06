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


def run_evaluation():
    keywords = get_keywords("data/keywords.txt")

    models = ["parakeet", "canary", "whisper", "parakeet_finetuned"]

    wers = {model: [] for model in models}
    keyword_errors = {model: [] for model in models}

    for filename in sorted(os.listdir("out/real")):
        if filename.endswith(".txt"):
            real_file = os.path.join("out/real", filename)
            for model in models:
                predicted_file = os.path.join(f"out/{model}", filename)
                wers[model].append(evaluate_transcriptions(real_file, predicted_file))
                keyword_errors[model].append(get_error_rate(real_file, predicted_file, keywords))

    for model in models:
        print(f"Average {model.capitalize()} WER: {sum(wers[model]) / len(wers[model]):.2%}")
    for model in models:
        print(f"Average {model.capitalize()} keyword error rate: {sum(keyword_errors[model]) / len(keyword_errors[model]):.2%}")


if __name__ == "__main__":
    run_evaluation()
