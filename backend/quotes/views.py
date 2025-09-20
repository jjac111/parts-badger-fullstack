import io
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from .tasks import ping, process_csv_upload
from .serializers import UploadCsvSerializer
from .services.csv_parser import CsvFormatError, parse_csv
from celery.result import AsyncResult


@api_view(["POST"])
def celery_health(_request):
    result = ping.delay()
    return Response({"task_id": result.id}, status=status.HTTP_202_ACCEPTED)


@api_view(["POST"])
def upload_csv(request: Request):
    serializer = UploadCsvSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    file_obj = serializer.validated_data["file"]
    content = file_obj.read()
    # Validate header early for fast feedback
    try:
        parse_csv(io.BytesIO(content))
    except CsvFormatError as exc:
        return Response({"error": str(exc)}, status=status.HTTP_400_BAD_REQUEST)

    task = process_csv_upload.delay(content, file_name=getattr(file_obj, "name", "upload.csv"))
    return Response({"task_id": task.id}, status=status.HTTP_202_ACCEPTED)


@api_view(["GET"])
def task_status(_request: Request, task_id: str):
    result = AsyncResult(task_id)
    return Response({
        "task_id": task_id,
        "state": result.state,
        "info": result.info if isinstance(result.info, dict) else str(result.info) if result.info else None,
    })
