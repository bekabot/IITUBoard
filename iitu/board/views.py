from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Record, User
from .serializers import RecordSerializer


class BoardView(APIView):
    def get(self, request):
        records = Record.objects.all()
        serializer = RecordSerializer(records, many=True)
        return Response({"records": serializer.data})

    def post(self, request):
        record = request.data.get('record')

        serializer = RecordSerializer(data=record)
        if serializer.is_valid(raise_exception=True):
            record_new = serializer.save()
        return Response({"success": "Record '{}' created successfully".format(record_new.text)})


class LoginView(APIView):
    def post(self, request):
        login = request.data.get('login')
        password = request.data.get('password')
        data = User.objects.filter(login=login, password=password, is_active=True).values()
        if len(data) == 0:
            return Response({
                "error": "THIS_USER_NOT_FOUND"
            })
        else:
            return JsonResponse(data[0])
