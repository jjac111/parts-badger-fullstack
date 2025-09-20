from rest_framework import serializers


class UploadCsvSerializer(serializers.Serializer):
    file = serializers.FileField()
