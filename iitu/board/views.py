from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Record
from .serializers import RecordSerializer


# Create your views here.
def index(request):
    return HttpResponse("Hello, Bitch!")


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
