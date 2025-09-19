from celery import shared_task


@shared_task(bind=True)
def ping(self):
    return {"ok": True}
