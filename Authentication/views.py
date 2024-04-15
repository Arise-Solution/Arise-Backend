import datetime
import random
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from Authentication.helper import MessageHandler, EmailHandler
from Authentication.models import MessageOTP, EmailOTP
from Authentication.serializers import MessageOTPSerializer, EmailOTPSerializer


class MessageOTPSend(APIView):
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
    @staticmethod
    def put(request):
        user = MessageOTP.objects.get(phone_number=request.data['phone'], user=request.data['user'])
        if user.otp == request.data['otp']:
            MessageOTP.objects.filter(phone_number=request.data['phone']).update(validated=True)
            return Response({'message': 'OTP verified successfully'}, status=status.HTTP_200_OK)
        return Response({'message': 'OTP verification failed'}, status=status.HTTP_400_BAD_REQUEST)


class MessageOTPResend(APIView):
    @staticmethod
    def post(request):
        user = MessageOTP.objects.get(phone_number=request.data['phone'], user=request.data['user'])
        if user.validated:
            return Response({'message': 'OTP already verified'}, status=status.HTTP_400_BAD_REQUEST)
        otp = random.randint(1000000, 9999999)
        MessageHandler(request.data['phone'], otp).send_otp_via_message()
        MessageOTP.objects.filter(phone_number=request.data['phone']).update(otp=f'{otp}')
        return Response({'message': 'OTP resent successfully'}, status=status.HTTP_200_OK)


class EmailOTPSend(APIView):
    @staticmethod
    def post(request):
        serializer = EmailOTPSerializer(data=request.data)
        end_week = datetime.date.today() + datetime.timedelta(-14)
        last_updated = EmailOTP.objects.filter(user=request.user).values('datetime')
        if (last_updated - end_week).days < 14:
            return Response({'message': (last_updated - end_week).days}, status=status.HTTP_400_BAD_REQUEST)
        if serializer.is_valid():
            otp = random.randint(1000000, 9999999)
            serializer.save(otp=f'{otp}')
            EmailHandler(request.data['email'], otp).send_otp_via_email()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmailOTPVerify(APIView):
    @staticmethod
    def put(request):
        user = EmailOTP.objects.get(email=request.data['email'], user=request.data['user'])
        if user.otp == request.data['otp']:
            EmailOTP.objects.filter(email=request.data['email']).update(validated=True)
            return Response({'message': 'OTP verified successfully'}, status=status.HTTP_200_OK)
        return Response({'message': 'OTP verification failed'}, status=status.HTTP_400_BAD_REQUEST)


class EmailOTPResend(APIView):
    @staticmethod
    def post(request):
        user = EmailOTP.objects.get(email=request.data['email'], user=request.data['user'])
        if user.validated:
            return Response({'message': 'OTP already verified'}, status=status.HTTP_400_BAD_REQUEST)
        otp = random.randint(1000000, 9999999)
        EmailHandler(request.data['email'], otp).send_otp_via_email()
        EmailOTP.objects.filter(email=request.data['email']).update(otp=f'{otp}')
        return Response({'message': 'OTP resent successfully'}, status=status.HTTP_200_OK)


class SignUpView(APIView):
    @staticmethod
    def post(request, *args, **kwargs):
        username = request.data['username']
        password = request.data['password']
        if not username or not password:
            return Response({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.create_user(username=username, password=password)
        if user:
            return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'Failed to create user'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LoginView(APIView):
    @staticmethod
    def post(request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    @staticmethod
    def post(request):
        request.session.flush()
        return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)

