import argparse
import errno
import sys
import os


LOGFIND_RC = os.path.expanduser('~/.logfind')


def get_important_files(logfind_rc=LOGFIND_RC):
    try:
        with open(logfind_rc) as f:
            important_files = [os.path.expanduser(path.strip()) for path in f if path]
    except IOError as e:
        if e.errno == errno.ENOENT:
            sys.exit('configuration missing at %r' % logfind_rc)
        raise
    return important_files


def scan_file(file_object, search_terms, and_lookup=True):
    search_term_set = set(search_terms)
    file_is_a_hit = False
    for line in file_object:
        present_term_set = {term for term in search_term_set if term in line}
        if and_lookup:
            search_term_set -= present_term_set
            file_is_a_hit = not search_term_set
        else:
            file_is_a_hit = bool(present_term_set)

        if file_is_a_hit:
            return True


def scan_file_path(file_path, search_terms, and_lookup=True):
    try:
        with open(file_path) as f:
            return scan_file(f, search_terms, and_lookup=and_lookup)
    except IOError as e:
        # Silently skip if the file does not exist
        if not e.errno == errno.ENOENT:
            raise


def get_args():
    parser = argparse.ArgumentParser(description='Scan files for search terms')
    parser.add_argument('words', metavar='word', type=str, nargs='+', help='search for these words in each file. Assumes AND between each word')
    parser.add_argument('-o', '--or-lookup', help='assume OR between each word', action='store_true')
    args = parser.parse_args()
    return args


def main():
    args = get_args()
    words = args.words
    and_lookup = not args.or_lookup
    paths_to_scan = get_important_files()
    hits = [path for path in paths_to_scan if scan_file_path(path, words, and_lookup=and_lookup)]
    for hit in hits:
        print(hit)
