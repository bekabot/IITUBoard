import hashlib
import os
import smtplib
from email.header import Header
from email.mime.text import MIMEText
from uuid import uuid4

from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.utils.crypto import get_random_string
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Record, User, FCMToken
from .serializers import RecordSerializer


class BoardView(APIView):
    def get(self, request):
        records = Record.objects.all()
        serializer = RecordSerializer(records, many=True)
        return Response({"records": serializer.data})

    # TODO check if id gets generated after it is saved and check for user token
    # TODO if null is not accepted by client, try this https://bit.ly/2Wj9gEq
    def post(self, request):
        record = request.data.get('record')

        serializer = RecordSerializer(data=record)
        if serializer.is_valid(raise_exception=True):
            record_new = serializer.save()
        return Response({"success": "Record '{}' created successfully".format(record_new.text)})


class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        fcm_token = request.data.get('fcmToken')
        data = User.objects.filter(email=email, password=password, is_active=True).values()
        if len(data) == 0:
            return Response({
                "error": "THIS_USER_NOT_FOUND"
            })
        else:
            FCMToken.objects.create(email=email, fcm_token=fcm_token)
            return JsonResponse(data[0])


class AuthView(APIView):
    def post(self, request):
        name = request.data.get('name')
        surname = request.data.get('surname')
        email = request.data.get('email')
        password = request.data.get('password')
        if settings.DEBUG:
            host = "http://127.0.0.1:8000"
        else:
            host = "http://iitu-board.herokuapp.com"

        mail_header = "Подтверждение почтового ящика"

        if email.endswith("@iitu.kz"):
            try:
                user = User.objects.get(email=email)
                if not user.is_active:
                    message_body = host + "/api/verify?token=" + user.token
                    send_mail(email, message_body, mail_header)
                    return Response({
                        "message": "MAIL_SENT"
                    })
                else:
                    return Response({
                        "message": "USER_ALREADY_EXISTS"
                    })
            except User.DoesNotExist:
                new_token = generate_token()
                User.objects.create(name=name, surname=surname, password=password, email=email, token=new_token,
                                    is_active=False)
                message_body = "Для активации аккаунта пройдите по ссылке:\n" + host + "/api/verify?token=" + new_token
                send_mail(email, message_body, mail_header)
                return Response({
                    "message": "MAIL_SENT"
                })
        else:
            return Response({
                "message": "WRONG_EMAIL"
            })


def generate_token():
    return str(uuid4())


def send_mail(receipent_mail, message_body, header_title):
    sender_address = os.environ.get('SMTP_SENDER')

    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.login(sender_address, os.environ.get('SMTP_PASSWORD'))

    msg = MIMEText(message_body, 'plain', 'utf-8')
    msg['Subject'] = Header(header_title, 'utf-8')
    msg['From'] = sender_address
    msg['To'] = receipent_mail

    server.sendmail(sender_address, receipent_mail, msg.as_string())
    server.quit()


class VerificationView(APIView):
    def get(self, request):
        token = request.query_params.get('token')
        try:
            user = User.objects.get(token=token)
            if not user.is_active:
                User.objects.filter(token=token).update(is_active=True)
                return HttpResponse("Почтовый адрес успешно подтвержден")
            else:
                return HttpResponse("Пользователь уже существует")
        except User.DoesNotExist:
            return HttpResponse("Пользователь не найден")


class RestoreView(APIView):
    def post(self, request):
        email = request.data.get('email')
        try:
            user = User.objects.get(email=email)
            if not user.is_active:
                return Response({
                    "message": "USER_NOT_ACTIV"
                })
            else:
                new_password = get_random_string(10)
                send_mail(email, "Ваш новый пароль - " + new_password, "Новый пароль IITU Connect")
                hashed_password = hashlib.sha256(new_password.encode('utf-8')).hexdigest()
                User.objects.filter(email=email).update(password=hashed_password)

                return Response({
                    "message": "PASSWORD_SENT"
                })
        except User.DoesNotExist:
            return Response({
                "message": "MAIL_NOT_FOUND"
            })
