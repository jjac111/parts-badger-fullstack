import io
import decimal
import pytest

from quotes.tasks import process_csv_upload


def test_process_csv_upload_calls_pipeline(monkeypatch):
    calls = {"parsed": None, "aggregated": None, "persisted": None}

    def fake_parse(file_obj):
        assert isinstance(file_obj, io.BytesIO)
        calls["parsed"] = True
        return ["AAA", "BBB"]

    def fake_aggregate(stock_codes):
        assert stock_codes == ["AAA", "BBB"]
        calls["aggregated"] = True
        return {
            "AAA": {"count": 1, "total_price": decimal.Decimal("1.00")},
            "BBB": {"count": 0, "total_price": decimal.Decimal("0.00")},
        }

    class FakeObj:
        def __init__(self, code):
            self.stock_code = code

    def fake_persist(results, file_name: str):
        assert file_name == "upload.csv"
        calls["persisted"] = True
        return [FakeObj("AAA"), FakeObj("BBB")]

    # Patch where used (module-level imported names inside quotes.tasks)
    monkeypatch.setattr("quotes.tasks.parse_csv", fake_parse)
    monkeypatch.setattr("quotes.tasks.aggregate_quotes", fake_aggregate)
    monkeypatch.setattr("quotes.tasks.persist_results", fake_persist)

    out = process_csv_upload.run(b"stock_code\nAAA\nBBB\n", file_name="upload.csv")
    assert out == {"created": 2}
    assert all(calls.values())
