import pytest
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_celery_health_enqueues_ping(monkeypatch):
    client = APIClient()

    class FakeAsyncResult:
        def __init__(self):
            self.id = "fake-task-id"

    def fake_delay():
        return FakeAsyncResult()

    import quotes.tasks as tasks

    monkeypatch.setattr(tasks.ping, "delay", fake_delay)

    resp = client.post("/health/celery/")
    assert resp.status_code == 202
    body = resp.json()
    assert body["task_id"] == "fake-task-id"
