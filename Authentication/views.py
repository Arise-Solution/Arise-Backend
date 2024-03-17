import datetime
import random
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.views.generic import RedirectView
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import MessageOTPSerializer, SignupVerificationSerializer
from .models import MessageOTP
from .helper import MessageHandler


class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    # callback_url = CALLBACK_URL_YOU_SET_ON_GOOGLE
    client_class = OAuth2Client


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return "redirect-url"


class MessageOTPSend(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request):
        serializer = MessageOTPSerializer(data=request.data)
        end_week = datetime.date.today() + datetime.timedelta(-14)
        last_updated = MessageOTP.objects.filter(user=request.user).values('datetime')
        if (last_updated - end_week).days < 14:
            return Response({'message': (last_updated - end_week).days}, status=status.HTTP_400_BAD_REQUEST)
        if serializer.is_valid():
            otp = random.randint(1000000, 9999999)
            serializer.save(otp=f'{otp}')
            MessageHandler(request.data['phone'], otp).send_otp_via_message()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MessageOTPVerify(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def put(request):
        user = MessageOTP.objects.get(phone_number=request.data['phone'], user=request.data['user'])
        if user.otp == request.data['otp']:
            MessageOTP.objects.filter(phone_number=request.data['phone']).update(validated=True)
            return Response({'message': 'OTP verified successfully'}, status=status.HTTP_200_OK)
        return Response({'message': 'OTP verification failed'}, status=status.HTTP_400_BAD_REQUEST)


class MessageOTPResend(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request):
        user = MessageOTP.objects.get(phone_number=request.data['phone'], user=request.data['user'])
        if user.validated:
            return Response({'message': 'OTP already verified'}, status=status.HTTP_400_BAD_REQUEST)
        otp = random.randint(1000000, 9999999)
        MessageHandler(request.data['phone'], otp).send_otp_via_message()
        MessageOTP.objects.filter(phone_number=request.data['phone']).update(otp=f'{otp}')
        return Response({'message': 'OTP resent successfully'}, status=status.HTTP_200_OK)


class SignupVerificationView(APIView):
    @staticmethod
    def post(request, *args, **kwargs):
        serializer = SignupVerificationSerializer(data=request.data)
        if serializer.is_valid():
            username_taken = User.objects.filter(username=serializer.validated_data['username']).exists()
            email_taken = User.objects.filter(email=serializer.validated_data['email']).exists()
            if username_taken:
                return Response({'detail': 'Username is already taken.'}, status=status.HTTP_400_BAD_REQUEST)
            if email_taken:
                return Response({'detail': 'Email is already taken.'}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'detail': 'Signup details are valid.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
