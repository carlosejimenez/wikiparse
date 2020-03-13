import os
import argparse
from datetime import datetime
import logging
from multiprocessing import Pool
import numpy as np
import spacy
import ujson
import utils


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


def run(thread_idxs):
    """
    For a single thread, extracts parsed relationships as lists of ujson strings. Saved to
    OUTPUTDIR/output_thread_num.json

    Args:
        thread_idxs (tuple): tuples of (thread_number, [idxs]) with thread_number used in conjunction with
        multiprocessing.Pool, to separate output for each thread. [idxs] is an iterable of article numbers as files in
        ARTICLES_DIR/. [idx] is a unique list for each thread_number.

    Returns:
        Time calculated to process all assigned articles.
    """
    thread_number, idxs = thread_idxs
    nlp = spacy.load('en_core_web_lg')
    start = datetime.now()
    total_idxs = len(idxs)
    outfile = open(ROOT + '/output_' + str(thread_number) + '.json', 'w')
    outfile.write('[')
    line_buffer = []
    for i_x, (_, article) in enumerate(utils.gen_articles_form_list(ARTICLES_DIR, idxs)):
        if article:
            parsed_article = nlp(article)
            line_buffer.extend(format_output(parsed_article))
            if (i_x + 1) % 5000 == 0:
                if line_buffer:
                    outfile.write(','.join(line_buffer))
                    outfile.write(',')
                    line_buffer = []
                logging.info(f'thread: {thread_number} ({i_x} / {total_idxs}) - {(100 * (i_x / total_idxs)):.2f} % complete')
    if line_buffer:
        outfile.write(','.join(line_buffer))
        outfile.write(']')
        line_buffer = []
    else:
        outfile.write('[]]')  # if no line_buffer, list ends with `,'
    outfile.close()
    logging.info(f'thread: {thread_number} - Complete')   
    total = (datetime.now() - start).seconds
    return total


def main(filename, num_threads):
    all_idxs = np.array([w.strip() for w in open(filename, 'r').readlines()])
    idxs_list = np.array_split(all_idxs, num_threads)
    pool = Pool(num_threads)
    times = pool.map(run, zip(range(num_threads), idxs_list))
    logging.info(f'Mean Article Time: %f seconds', (sum(times) / len(all_idxs)))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--articles-dir', type=str, help='filename/path for main articles directory. (ie. output of \
    extract_docs.py)')
    parser.add_argument('-f', '--idx-filename', type=str, help='filename/path for list of article idxs to parse. (ie. \
    output of get_idxs.py)')
    parser.add_argument('-c', '--cpu-count', type=int, help='Number of CPUs to use.')
    parser.add_argument('-o', '--output-dir', type=str, help='Directory name for distributed output.')
    args = parser.parse_args()
    ROOT = os.path.abspath(args.output_dir)
    ARTICLES_DIR = os.path.abspath(args.articles_dir)
    INIT = datetime.now()
    os.makedirs(ROOT, exist_ok=True)
    logging.basicConfig(level=logging.INFO)
    main(args.idx_filename, args.cpu_count)
    logging.info(f'Total time: %d seconds ...', (datetime.now() - INIT).seconds)
