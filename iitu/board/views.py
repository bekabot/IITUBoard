import os
import smtplib
from email.header import Header
from email.mime.text import MIMEText
from uuid import uuid4

from django.conf import settings
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


class AuthView(APIView):
    def post(self, request):
        login = request.data.get('login')
        password = request.data.get('password')
        email = request.data.get('email')
        if email.endswith("@iitu.kz"):
            try:
                user = User.objects.get(login=login)
                if not user.is_active:
                    User.objects.filter(login=login).update(email=email)
                    send_email_with_token(email, user.token)
                    return Response({
                        "message": "MAIL_SENT"
                    })
                else:
                    return Response({
                        "error": "USER_ALREADY_EXISTS"
                    })
            except User.DoesNotExist:
                new_token = generate_token()
                User.objects.create(login=login, password=password, email=email, token=new_token, is_active=False)
                send_email_with_token(email, new_token)
                return Response({
                    "message": "MAIL_SENT"
                })
        else:
            return Response({
                "error": "WRONG_EMAIL"
            })


def generate_token():
    return str(uuid4())


def send_email_with_token(receipent_mail, token):
    if settings.DEBUG:
        host = "http://127.0.0.1:8000"
    else:
        host = "http://iitu-board.herokuapp.com"

    sender_address = os.environ.get('SMTP_SENDER')

    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.login(sender_address, os.environ.get('SMTP_PASSWORD'))
    message_body = host + "/verify?token=" + token

    msg = MIMEText(message_body, 'plain', 'utf-8')
    msg['Subject'] = Header("Подтверждение почтового ящика", 'utf-8')
    msg['From'] = sender_address
    msg['To'] = sender_address

    # TODO uncomment to test on @iitu.kz mail
    # server.sendmail(sender_address, receipent_mail, msg.as_string())
    server.sendmail(sender_address, sender_address, msg.as_string())
    server.quit()
