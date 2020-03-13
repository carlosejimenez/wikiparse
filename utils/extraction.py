import numpy as np
import ujson


def format_output(doc):
    """
    Return a json string of the parsed values. Ex. tuple of list of verbs in sentences.
    Args:
        doc: spacy Doc type, with sents attribute.

    Returns:
        tuple of json-strings. 
    """
    sentences = []
    for sent in doc.sents:
        verbs = [w.text for w in sent if w.pos_ == 'VERB']
        sentences.append(ujson.dumps(verbs))
    return tuple(sentences)

