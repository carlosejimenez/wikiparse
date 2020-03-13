import numpy as np
import ujson


def format_output(doc):
    sentences = []
    for sent in doc.sents:
        sentences.append(sent.root)
    return tuple(sentences)

