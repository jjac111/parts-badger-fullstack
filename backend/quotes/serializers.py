from rest_framework import serializers


class UploadCsvSerializer(serializers.Serializer):
    file = serializers.FileField()


class CsvResultSerializer(serializers.Serializer):
    stock_code = serializers.CharField()
    number_quotes_found = serializers.IntegerField()
    total_price = serializers.DecimalField(max_digits=12, decimal_places=2)
    file_uploaded = serializers.CharField()
    created_at = serializers.DateTimeField()
