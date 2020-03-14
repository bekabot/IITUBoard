from rest_framework import serializers

from .models import Record


class RecordSerializer(serializers.Serializer):
    record_title = serializers.CharField(max_length=100)
    record_body = serializers.CharField(max_length=10000)
    image1 = serializers.ImageField(max_length=None, use_url=True, allow_null=True,
                                    required=False)  # todo rename to eng symbols
    image2 = serializers.ImageField(max_length=None, use_url=True, allow_null=True,
                                    required=False)  # todo rename to eng symbols
    image3 = serializers.ImageField(max_length=None, use_url=True, allow_null=True,
                                    required=False)  # todo rename to eng symbols

    def create(self, validated_data):
        return Record.objects.create(**validated_data)
