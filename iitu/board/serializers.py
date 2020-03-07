from rest_framework import serializers

from .models import Record


class RecordSerializer(serializers.Serializer):
    text = serializers.CharField(max_length=2000)

    def create(self, validated_data):
        return Record.objects.create(**validated_data)
