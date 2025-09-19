import decimal
import pytest

from quotes.models import CsvResult
from quotes.services.persist import persist_results


@pytest.mark.django_db
def test_persist_results_creates_rows_and_returns_objects():
    results = {
        "AAA": {"count": 2, "total_price": decimal.Decimal("10.50")},
        "BBB": {"count": 0, "total_price": decimal.Decimal("0.00")},
    }

    created = persist_results(results, file_name="upload.csv")

    assert len(created) == 2
    rows = {r.stock_code: r for r in CsvResult.objects.all()}
    assert rows["AAA"].number_quotes_found == 2
    assert rows["AAA"].total_price == decimal.Decimal("10.50")
    assert rows["AAA"].file_uploaded == "upload.csv"
    assert rows["BBB"].number_quotes_found == 0
    assert rows["BBB"].total_price == decimal.Decimal("0.00")


@pytest.mark.django_db
def test_persist_results_quantizes_decimals():
    results = {
        "CCC": {"count": 1, "total_price": decimal.Decimal("1.999")},
    }
    created = persist_results(results, file_name="upload2.csv")
    assert created[0].total_price == decimal.Decimal("2.00")
