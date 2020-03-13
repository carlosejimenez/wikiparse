import pickle
import os
import spacy
import pandas as pd


def gen_articles_form_list(articles_dir, idx_list):
    for idx in idx_list:
        yield idx, ' '.join(open(articles_dir + '/' + idx, 'r').readlines()[1:])
 

def gen_articles(articles_dir):
    return gen_articles_form_list(articles_dir, get_articles_idxs())

