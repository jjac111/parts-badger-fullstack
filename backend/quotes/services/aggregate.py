import decimal
from typing import Iterable
from django.db.models import Sum, Count

from quotes.models import Part, QuoteLineItem


def aggregate_quotes(stock_codes: Iterable[str]):
    stock_codes = list(stock_codes)
    # Defaults for all requested codes
    result = {
        code: {"count": 0, "total_price": decimal.Decimal("0.00")} for code in stock_codes
    }

    if not stock_codes:
        return result

    parts = Part.objects.filter(stock_code__in=stock_codes).values_list("id", "stock_code")  # type: ignore[attr-defined]
    part_id_to_code = {pid: code for pid, code in parts}

    if not part_id_to_code:
        return result

    aggregates = (
        QuoteLineItem.objects.filter(part_id__in=part_id_to_code.keys())  # type: ignore[attr-defined]
        .values("part_id")
        .annotate(
            count=Count("quote", distinct=True),
            total_price=Sum("price"),
        )
    )

    for row in aggregates:
        code = part_id_to_code[row["part_id"]]
        total_price = row["total_price"] or decimal.Decimal("0.00")
        # Ensure 2-decimal places
        total_price = total_price.quantize(decimal.Decimal("0.00"))
        result[code] = {"count": row["count"], "total_price": total_price}

    return result
