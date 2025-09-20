import decimal
import pytest

from quotes.models import Part, Quote, QuoteLineItem
from quotes.services.aggregate import aggregate_quotes


@pytest.mark.django_db
def test_aggregate_returns_zero_for_missing_parts():
    result = aggregate_quotes(["NOPE1", "NOPE2"])  # none exist
    assert result == {
        "NOPE1": {"count": 0, "total_price": decimal.Decimal("0.00")},
        "NOPE2": {"count": 0, "total_price": decimal.Decimal("0.00")},
    }


@pytest.mark.django_db
def test_aggregate_counts_and_sums_per_stock_code():
    part_a = Part.objects.create(stock_code="AAA", description="a")
    part_b = Part.objects.create(stock_code="BBB", description="b")
    q1 = Quote.objects.create(name="Q1", status="approved")
    q2 = Quote.objects.create(name="Q2", status="approved")
    QuoteLineItem.objects.create(quote=q1, part=part_a, quantity=1, price=decimal.Decimal("10.50"))
    QuoteLineItem.objects.create(quote=q1, part=part_a, quantity=2, price=decimal.Decimal("5.50"))
    QuoteLineItem.objects.create(quote=q2, part=part_b, quantity=3, price=decimal.Decimal("2.00"))

    result = aggregate_quotes(["AAA", "BBB", "CCC"])  # CCC has no part

    # Distinct quotes for AAA: both items on q1 count as 1
    assert result["AAA"]["count"] == 1
    assert result["AAA"]["total_price"] == decimal.Decimal("16.00")
    assert result["BBB"]["count"] == 1
    assert result["BBB"]["total_price"] == decimal.Decimal("2.00")
    assert result["CCC"]["count"] == 0
    assert result["CCC"]["total_price"] == decimal.Decimal("0.00")
