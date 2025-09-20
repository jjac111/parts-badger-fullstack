import pytest
from rest_framework.test import APIClient


def test_get_task_status_returns_state(monkeypatch):
    client = APIClient()

    class FakeAsyncResult:
        def __init__(self, task_id):
            self.id = task_id
            self.state = "SUCCESS"
            self.info = {"created": 2}

    def fake_async_result(task_id):
        return FakeAsyncResult(task_id)

    import quotes.views as views
    monkeypatch.setattr(views, "AsyncResult", fake_async_result)

    resp = client.get("/tasks/task-xyz/")
    assert resp.status_code == 200
    body = resp.json()
    assert body["task_id"] == "task-xyz"
    assert body["state"] == "SUCCESS"
    assert body["info"] == {"created": 2}


def test_get_task_status_requires_task_id():
    client = APIClient()
    resp = client.get("/tasks//")
    assert resp.status_code in (400, 404)
