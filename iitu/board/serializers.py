from rest_framework import serializers

from .models import Record, User


class RecordSerializer(serializers.Serializer):
    text = serializers.CharField(max_length=2000)

    def create(self, validated_data):
        return Record.objects.create(**validated_data)

#TODO not used
class UserSerializer(serializers.Serializer):
    class Meta:
        model = User
        fields = (
            'login', 'email', 'token'
        )
    login = serializers.CharField(max_length=20)
    email = serializers.CharField(max_length=30)
    token = serializers.CharField(max_length=100)

    def create(self, validated_data):
        return User.objects.create(**validated_data)
