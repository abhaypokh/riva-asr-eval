import spacy

nlp = spacy.load("en_core_web_sm")


def anonymize(transcript_text, placeholder="<PERSON>"):
    doc = nlp(transcript_text)
    spans = [(ent.start_char, ent.end_char) for ent in doc.ents if ent.label_ == "PERSON"]
    for start_char, end_char in sorted(spans, reverse=True):
        transcript_text = transcript_text[:start_char] + placeholder + transcript_text[end_char:]
    return transcript_text


if __name__ == "__main__":
    text = "Hi, my name is John Smith. Hello John, how can I help you?"
    print(anonymize(text))
