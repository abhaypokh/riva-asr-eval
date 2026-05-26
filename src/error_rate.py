def get_keywords(filename):
    with open(filename, "r") as f:
        text = f.read().lower()
    keywords = set()
    for line in text.split("\n"):
        line = line.strip()
        if line and not line.startswith("#"):
            keywords.add(line)
    return keywords


def get_error_rate(reference_file, hypothesis_file, keywords):
    with open(reference_file, "r") as f:
        reference = f.read().lower()
    with open(hypothesis_file, "r") as f:
        hypothesis = f.read().lower()
    correct = 0
    total = 0
    for word in keywords:
        reference_count = reference.count(word)
        total += reference_count
        correct += min(reference_count, hypothesis.count(word))
    return 1 - (correct / total) if total > 0 else 0


if __name__ == "__main__":
    print(get_keywords("data/keywords.txt"))