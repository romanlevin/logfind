import logfind
import tempfile
from contextlib import contextmanager


@contextmanager
def mock_file(contents):
    with tempfile.NamedTemporaryFile() as f:
        f.write(contents)
        f.flush()
        yield f


def test_scan_file_positive_and():
    mock_file_contents = b"""
term1
term3
term2
"""
    terms = (b'term1', b'term2')
    patterns = logfind.compile_patterns(terms)
    with mock_file(mock_file_contents) as f:
        result = logfind.scan_file(f, patterns)
    assert result


def test_scan_file_negative_and():
    mock_file_contents = b"""
term1
term3
"""
    terms = (b'term1', b'term2')
    patterns = logfind.compile_patterns(terms)
    with mock_file(mock_file_contents) as f:
        result = logfind.scan_file(f, patterns)
    assert not result


def test_scan_file_positive_or():
    mock_file_contents = b"""
term1
"""
    terms = (b'term1', b'term2')
    patterns = logfind.compile_patterns(terms)
    with mock_file(mock_file_contents) as f:
        result = logfind.scan_file(f, patterns, and_lookup=False)
    assert result


def test_scan_file_negative_or():
    mock_file_contents = b"""
term3
"""
    terms = (b'term1', b'term2')
    patterns = logfind.compile_patterns(terms)
    with mock_file(mock_file_contents) as f:
        result = logfind.scan_file(f, patterns, and_lookup=False)
    assert not result
