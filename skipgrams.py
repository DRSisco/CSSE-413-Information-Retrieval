def skipbigrams(text):
    bigrams = list()
    for i in range(0, len(text)-2):
        bigrams.append((text[i], text[i+2]))
    return bigrams