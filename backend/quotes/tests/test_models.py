import decimal
import pytest
from django.db import IntegrityError

from quotes.models import Part, Quote, QuoteLineItem, CsvResult


@pytest.mark.django_db
def test_part_unique_stock_code():
    Part.objects.create(stock_code="ABC123", description="Widget A")
    with pytest.raises(IntegrityError):
        Part.objects.create(stock_code="ABC123", description="Duplicate")


@pytest.mark.django_db
def test_quote_line_item_relations_and_decimal_precision():
    part = Part.objects.create(stock_code="ZZZ999", description="Thing")
    quote = Quote.objects.create(name="Q-1", status="pending")
    item = QuoteLineItem.objects.create(
        quote=quote,
        part=part,
        quantity=2,
        price=decimal.Decimal("12.34"),
    )
    assert item.quote_id == quote.id
    assert item.part_id == part.id
    assert item.price == decimal.Decimal("12.34")


@pytest.mark.django_db
def test_csv_result_creation_fields():
    result = CsvResult.objects.create(
        stock_code="ABC123",
        number_quotes_found=0,
        total_price=decimal.Decimal("0.00"),
        file_uploaded="sample.csv",
    )
    assert result.stock_code == "ABC123"
    assert result.total_price == decimal.Decimal("0.00")
    assert result.file_uploaded == "sample.csv"
