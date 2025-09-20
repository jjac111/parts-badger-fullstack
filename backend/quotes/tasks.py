from celery import shared_task
import io
from quotes.services.csv_parser import parse_csv
from quotes.services.aggregate import aggregate_quotes
from quotes.services.persist import persist_results


@shared_task(bind=True)
def ping(self):
    return {"ok": True}


@shared_task(bind=True)
def process_csv_upload(self, file_bytes: bytes, file_name: str):
    stock_codes = parse_csv(io.BytesIO(file_bytes))
    aggregates = aggregate_quotes(stock_codes)
    created = persist_results(aggregates, file_name=file_name)
    return {"created": len(created)}
