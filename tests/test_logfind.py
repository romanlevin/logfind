from io import StringIO
import logfind


def test_scan_file_positive_and():
    mock_file_contents = """
term1
term3
term2
"""
    terms = ('term1', 'term2')
    mock_file = StringIO(mock_file_contents)
    result = logfind.scan_file(mock_file, terms)
    assert result


def test_scan_file_negative_and():
    mock_file_contents = """
term1
term3
"""
    terms = ('term1', 'term2')
    mock_file = StringIO(mock_file_contents)
    result = logfind.scan_file(mock_file, terms)
    assert not result


def test_scan_file_positive_or():
    mock_file_contents = """
term1
"""
    terms = ('term1', 'term2')
    mock_file = StringIO(mock_file_contents)
    result = logfind.scan_file(mock_file, terms, and_lookup=False)
    assert result


def test_scan_file_negative_or():
    mock_file_contents = """
term3
"""
    terms = ('term1', 'term2')
    mock_file = StringIO(mock_file_contents)
    result = logfind.scan_file(mock_file, terms, and_lookup=False)
    assert not result
