import logfind
import tempfile
from contextlib import contextmanager


@contextmanager
def mock_file(contents):
    with tempfile.NamedTemporaryFile() as f:
        f.write(contents)
        f.flush()
        yield f


def scan_mock_file(contents, terms, and_lookup=True):
    patterns = logfind.compile_patterns(terms, and_lookup)
    with mock_file(contents) as f:
        return logfind.scan_file(f, patterns, and_lookup)


def test_scan_file_positive_and():
    mock_file_contents = b"""
term1
term3
term2
"""
    terms = (b'term1', b'term2')
    assert scan_mock_file(mock_file_contents, terms)


def test_scan_file_negative_and():
    mock_file_contents = b"""
term1
term3
"""
    terms = (b'term1', b'term2')
    assert not scan_mock_file(mock_file_contents, terms)


def test_scan_file_positive_or():
    mock_file_contents = b"""
term1
"""
    terms = (b'term1', b'term2')
    assert scan_mock_file(mock_file_contents, terms, and_lookup=False)


def test_scan_file_negative_or():
    mock_file_contents = b"""
term3
"""
    terms = (b'term1', b'term2')
    assert not scan_mock_file(mock_file_contents, terms, and_lookup=False)
