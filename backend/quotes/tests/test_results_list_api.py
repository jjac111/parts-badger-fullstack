import decimal
import pytest
from django.utils import timezone

from quotes.models import CsvResult
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_list_results_paginates_and_orders_desc():
    CsvResult.objects.create(stock_code="Z-1", number_quotes_found=1, total_price=decimal.Decimal("1.00"), file_uploaded="a.csv", created_at=timezone.now())
    CsvResult.objects.create(stock_code="A-2", number_quotes_found=2, total_price=decimal.Decimal("2.00"), file_uploaded="b.csv", created_at=timezone.now())

    client = APIClient()
    resp = client.get("/csv-results/")
    assert resp.status_code == 200
    body = resp.json()
    assert "results" in body
    # Most recent first by created_at desc
    assert body["results"][0]["stock_code"] in {"A-2", "Z-1"}


@pytest.mark.django_db
def test_list_results_filters_by_search():
    CsvResult.objects.create(stock_code="ABC1", number_quotes_found=1, total_price=decimal.Decimal("1.00"), file_uploaded="a.csv")
    CsvResult.objects.create(stock_code="DEF2", number_quotes_found=1, total_price=decimal.Decimal("1.00"), file_uploaded="b.csv")

    client = APIClient()
    resp = client.get("/csv-results/?search=ABC")
    assert resp.status_code == 200
    codes = [row["stock_code"] for row in resp.json()["results"]]
    assert codes == ["ABC1"]
