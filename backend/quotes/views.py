from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .tasks import ping


@api_view(["POST"])
def celery_health(_request):
    result = ping.delay()
    return Response({"task_id": result.id}, status=status.HTTP_202_ACCEPTED)

# Create your views here.
