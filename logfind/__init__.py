import argparse
import errno
import sys
import os
import re
import mmap


LOGFIND_RC = os.path.expanduser('~/.logfind')


def get_important_files(logfind_rc=LOGFIND_RC):
    try:
        with open(logfind_rc) as f:
            for path in f:
                if path:
                    yield os.path.expanduser(path.strip())
    except IOError as e:
        if e.errno == errno.ENOENT:
            sys.exit('configuration missing at %r' % logfind_rc)
        raise


def scan_file(file_object, patterns, and_lookup=True):
    with mmap.mmap(file_object.fileno(), 0) as data:
        return all(pattern.search(data) for pattern in patterns)


def scan_file_path(file_path, patterns, and_lookup=True):
    try:
        with open(file_path, 'r+b') as f:
            return scan_file(f, patterns, and_lookup=and_lookup)
    except IOError as e:
        # Silently skip if the file does not exist
        if not e.errno == errno.ENOENT:
            raise


def compile_patterns(patterns, and_lookup=True):
    return tuple(re.compile(p) for p in patterns) if and_lookup else (re.compile(b'|'.join(b'(' + p + b')' for p in patterns)),)


def get_args():
    str_to_byte = lambda s: s.encode('utf-8')
    parser = argparse.ArgumentParser(description='Scan files for search terms')
    parser.add_argument('patterns', metavar='pattern', type=str_to_byte, nargs='+', help='search for these regexp patterns in each file. Assumes AND between each pattern')
    parser.add_argument('-o', '--or-lookup', help='assume OR between each pattern', action='store_true')
    args = parser.parse_args()
    return args


def main():
    args = get_args()
    patterns = args.patterns
    and_lookup = not args.or_lookup
    paths_to_scan = get_important_files()
    compiled_patterns = compile_patterns(patterns, and_lookup=and_lookup)
    hits = [path for path in paths_to_scan if scan_file_path(path, compiled_patterns, and_lookup=and_lookup)]
    for hit in hits:
        print(hit)
