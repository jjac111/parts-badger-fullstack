import decimal
from typing import Dict

from quotes.models import CsvResult


def persist_results(results: Dict[str, dict], file_name: str):
    objects = []
    for stock_code, payload in results.items():
        count = int(payload.get("count", 0))
        total_price = decimal.Decimal(payload.get("total_price", "0.00"))
        total_price = total_price.quantize(decimal.Decimal("0.00"))
        objects.append(
            CsvResult(
                stock_code=stock_code,
                number_quotes_found=count,
                total_price=total_price,
                file_uploaded=file_name,
            )
        )
    created = CsvResult.objects.bulk_create(objects)
    return created
