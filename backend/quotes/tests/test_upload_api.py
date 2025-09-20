import pytest
from rest_framework.test import APIClient
from django.core.files.uploadedfile import SimpleUploadedFile
import io


@pytest.mark.django_db
def test_upload_csv_enqueues_task(monkeypatch):
    client = APIClient()

    class FakeAsyncResult:
        def __init__(self):
            self.id = "task-123"

    def fake_delay(file_bytes, file_name):
        assert b"stock_code" in file_bytes
        assert file_name == "test.csv"
        return FakeAsyncResult()

    import quotes.tasks as tasks
    monkeypatch.setattr(tasks.process_csv_upload, "delay", fake_delay)

    content = b"stock_code\nABC\n"
    upload = SimpleUploadedFile("test.csv", content, content_type="text/csv")
    resp = client.post("/upload-csv/", data={"file": upload}, format="multipart")
    assert resp.status_code == 202
    assert resp.json()["task_id"] == "task-123"


def test_upload_csv_requires_file():
    client = APIClient()
    resp = client.post("/upload-csv/", data={}, format="multipart")
    assert resp.status_code == 400
    assert "file" in resp.json()


def test_upload_csv_validates_header():
    client = APIClient()
    bad = b"not_stock_code\nABC\n"
    resp = client.post(
        "/upload-csv/",
        data={"file": io.BytesIO(bad)},
        format="multipart",
    )
    assert resp.status_code == 400
    assert resp.json()["error"]
