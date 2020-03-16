from rest_framework import serializers

from .models import Record


# TODO if null is not accepted by client, try this https://bit.ly/2Wj9gEq
class RecordSerializer(serializers.Serializer):
    record_title = serializers.CharField(max_length=200)
    record_body = serializers.CharField(max_length=10000)
    image1 = serializers.ImageField(max_length=None, use_url=True, allow_empty_file=True, required=False)
    image2 = serializers.ImageField(max_length=None, use_url=True, allow_null=True, required=False)
    image3 = serializers.ImageField(max_length=None, use_url=True, allow_null=True, required=False)
    phone = serializers.CharField(max_length=11)
    email = serializers.CharField(max_length=40)
    whatsapp = serializers.CharField(max_length=11)
    instagram = serializers.CharField(max_length=30)
    vk = serializers.CharField(max_length=30)
    telegram = serializers.CharField(max_length=30)
    record_type = serializers.CharField(max_length=7)
    ads_category = serializers.CharField(max_length=20)

    def create(self, validated_data):
        return Record.objects.create(**validated_data)
