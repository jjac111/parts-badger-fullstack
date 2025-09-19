import csv
import io


class CsvFormatError(ValueError):
    pass


def parse_csv(file_obj: io.BufferedIOBase) -> list[str]:
    raw = file_obj.read()
    if not raw:
        raise CsvFormatError("Empty file")
    text = raw.decode("utf-8", errors="strict")

    reader = csv.DictReader(io.StringIO(text))
    if not reader.fieldnames or "stock_code" not in [h.strip() for h in reader.fieldnames]:
        raise CsvFormatError("Missing required header: stock_code")

    seen = set()
    result: list[str] = []
    for row in reader:
        value = (row.get("stock_code") or "").strip()
        if not value:
            continue
        if value not in seen:
            seen.add(value)
            result.append(value)
    return result
