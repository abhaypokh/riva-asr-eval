import wave


def stitch(files, output_path):
    data = []
    for f in files:
        with wave.open(f, 'rb') as w:
            data.append([w.getparams(), w.readframes(w.getnframes())])

    with wave.open(output_path, 'wb') as output:
        output.setparams(data[0][0])
        for _, frames in data:
            output.writeframes(frames)
