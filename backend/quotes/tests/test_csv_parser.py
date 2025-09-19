import io
import pytest

from quotes.services.csv_parser import parse_csv, CsvFormatError


def _bytes(s: str) -> bytes:
    return s.encode("utf-8")


def test_parse_csv_requires_stock_code_header():
    data = _bytes("not_stock_code\nA\n")
    with pytest.raises(CsvFormatError):
        parse_csv(io.BytesIO(data))


def test_parse_csv_trims_and_dedupes_codes():
    data = _bytes("stock_code\n ABC123 \nabc123\n\nABC123\n")
    codes = parse_csv(io.BytesIO(data))
    assert codes == ["ABC123", "abc123"]


def test_parse_csv_empty_file():
    with pytest.raises(CsvFormatError):
        parse_csv(io.BytesIO(b""))
