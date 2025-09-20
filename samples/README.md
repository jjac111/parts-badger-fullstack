Sample CSVs for manual testing

Files:
- valid.csv
- missing_header.csv

Usage:
1. Seed demo data:
```
docker compose exec backend python manage.py seed_demo
```
2. Upload a sample via frontend or curl:
```
curl -X POST -F "file=@samples/valid.csv" http://localhost:8000/upload-csv/
```

