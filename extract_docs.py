import argparse
import re
import os

header = r'\<doc id\=(\"\d+\") url=(\".+\") title\=(\".+\")\>'
words_split_re = re.compile(r'[^\w\-\']')


def parse_all():
    with open('output.xml', 'r') as infile:
        article = []
        line = infile.readline()
        while line:
            if line.startswith('<doc '):
                idx, url, title = re.match(header, line.strip()).groups()
                idx = int(idx.strip('"'))
                # url = url.strip('"')
                # title = title.strip('"')
            elif line.startswith('</doc>'):
                with open(ARTICLES_DIR + '/' + str(idx), 'w') as outfile:
                    outfile.write(' '.join(article))
                article = []
            else:
                if line.strip():  # if line != '\n'
                    article.append(line)
            line = infile.readline()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--articles-dir', type=str, help='Articles directory path for output.')
    args = parser.parse_args()
    ARTICLES_DIR = os.path.abspath(args.articles_dir)
    os.makedirs(ARTICLES_DIR, exist_ok=True)
    parse_all()

