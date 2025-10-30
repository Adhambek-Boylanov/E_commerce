import random
from django.core.cache import cache
from django.core.mail import send_mail
from rest_framework.response import Response
from rest_framework.views import APIView
from configapp.models import User
from configapp.serializers import SendSmsSerializer,VerifySerializer
from drf_yasg.utils import swagger_auto_schema
from django.conf import settings
from configapp.make_token import get_tokens_for_user
class SendSmsApi(APIView):
    @swagger_auto_schema(request_body=SendSmsSerializer)
    def post(self,request):
        subject = "Ro'yxatdan o'tish kodi"
        serializer = SendSmsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        otp_kod = str(random.randint(10000,99999))
        email_from = settings.EMAIL_HOST_USER
        recipient_list =[email]
        cache.set(email,otp_kod,600)
        message = f"Sizning ruyhatdan otish kodingiz: {otp_kod}"
        send_mail(subject, message, email_from, recipient_list)
        return Response(data={f"{email}": "OTP yuborildi"})

class VerifyApi(APIView):
    @swagger_auto_schema(request_body=VerifySerializer)
    def post(self,request):
        serializer = VerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        verify_kod = serializer.validated_data['verify_kod']
        cache_kod = str(cache.get(email))
        if verify_kod == cache_kod:
            user,create = User.objects.get_or_create(email = email)
            if create:
                user.save()
            token = get_tokens_for_user(user)
            return Response(token)
        return Response({"message":"Invalid verify code"})