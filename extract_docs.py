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
                with open('./articles/' + str(idx), 'w+') as outfile:
                    outfile.write(' '.join(article))
                article = []
            else:
                if line.strip():  # if line != '\n'
                    article.append(line)
            line = infile.readline()


if __name__ == '__main__':
    os.makedirs('./articles', exist_ok=True)
    parse_all()

