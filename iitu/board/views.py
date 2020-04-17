import hashlib
import json
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
        token = request.query_params.get('token')
        record_id = request.query_params.get('id')
        try:
            user = User.objects.get(token=token)
            if user.is_active:
                records = Record.objects.all()
                if record_id is None:
                    serializer = RecordSerializer(records, many=True)
                    return Response({"records": serializer.data})
                else:
                    record = Record.objects.get(id=record_id)
                    serializer = RecordSerializer(record)
                    return Response({"record": serializer.data})
            else:
                return Response({
                    "message": "USER_NOT_ACTIV"
                })
        except User.DoesNotExist:
            return Response({
                "message": "USER_NOT_FOUND"
            })
        except Record.DoesNotExist:
            return Response({
                "message": "RECORD_NOT_FOUND"
            })

    def post(self, request):

        try:
            record = request.data.get('record')
            return self.handle_request_with_images(record, request)

        except TypeError:
            return self.handle_request_without_images(request)

    def handle_request_without_images(self, request):
        try:
            token = request.data.get('token')
            user = User.objects.get(token=token)
            if user.is_active:

                record_title = request.data.get('title', "")
                record_body = request.data.get('body', "")
                phone = request.data.get('phone', "")
                email = request.data.get('email', "")
                whatsapp = request.data.get('whatsapp', "")
                instagram = request.data.get('instagram', "")
                vk = request.data.get('vk', "")
                telegram = request.data.get('telegram', "")
                record_type = request.data.get('record_type', "news")
                author = request.data.get('author', "")

                new_record = Record()
                new_record.record_title = record_title
                new_record.record_body = record_body
                new_record.phone = phone
                new_record.email = email
                new_record.whatsapp = whatsapp
                new_record.instagram = instagram
                new_record.vk = vk
                new_record.telegram = telegram
                new_record.record_type = record_type
                new_record.author = author

                try:
                    new_record.save()
                except OSError:
                    return Response({
                        "message": "RECORD_NOT_CREATED"
                    })

                return Response({
                    "message": "RECORD_CREATED"
                })
            else:
                return Response({
                    "message": "USER_NOT_ACTIV"
                })
        except User.DoesNotExist:
            return Response({
                "message": "USER_NOT_FOUND"
            })

    def handle_request_with_images(self, record, request):
        record_dict = json.loads(record)
        token = record_dict.get('token')
        try:
            user = User.objects.get(token=token)
            if user.is_active:

                record_title = record_dict.get('title', "")
                record_body = record_dict.get('body', "")
                phone = record_dict.get('phone', "")
                email = record_dict.get('email', "")
                whatsapp = record_dict.get('whatsapp', "")
                instagram = record_dict.get('instagram', "")
                vk = record_dict.get('vk', "")
                telegram = record_dict.get('telegram', "")
                record_type = record_dict.get('record_type', "news")
                author = record_dict.get('author', "")

                new_record = Record()
                new_record.record_title = record_title
                new_record.record_body = record_body

                try:
                    image1 = request.FILES.getlist('file')[0]
                    new_record.image1 = image1
                except:
                    pass

                try:
                    image2 = request.FILES.getlist('file')[1]
                    new_record.image2 = image2
                except:
                    pass

                try:
                    image3 = request.FILES.getlist('file')[2]
                    new_record.image3 = image3
                except:
                    pass

                new_record.phone = phone
                new_record.email = email
                new_record.whatsapp = whatsapp
                new_record.instagram = instagram
                new_record.vk = vk
                new_record.telegram = telegram
                new_record.record_type = record_type
                new_record.author = author

                try:
                    new_record.save()
                except OSError:
                    return Response({
                        "message": "RECORD_NOT_CREATED"
                    })

                return Response({
                    "message": "RECORD_CREATED"
                })
            else:
                return Response({
                    "message": "USER_NOT_ACTIV"
                })
        except User.DoesNotExist:
            return Response({
                "message": "USER_NOT_FOUND"
            })


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
            fcm_data = FCMToken.objects.filter(fcm_token=fcm_token)
            if len(fcm_data) == 0 and fcm_token is not None and len(fcm_token) > 0:
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
