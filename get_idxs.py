import argparse
import os


def condition(article):
    return len(article) > 1


def main(article_dir, outfile):
    all_idxs = os.listdir(article_dir)
    all_idxs = list(map(str, sorted(map(int, all_idxs))))
    
    valid_idxs = [idx for idx in all_idxs if condition(open(article_dir + '/' + idx, 'r').read())]

    with open(outfile, 'w+') as output:
        output.write('\n'.join(valid_idxs))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--article-dir', type=str, help='directory where articles are saved as idx numbers.')
    parser.add_argument('-o', '--output', type=str, help='filename to save valid idxs under. (ie. input for \
    run_parser.py)')
    args = parser.parse_args()
    main(os.path.abspath(args.article_dir), args.output)

