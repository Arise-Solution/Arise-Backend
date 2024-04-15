from rest_framework import serializers
from django.contrib.auth.models import User
from .models import MessageOTP, EmailOTP


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class MessageOTPSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = MessageOTP
        fields = ['id', 'user', 'phone_number', 'otp', 'create_date_time', 'validate_date_time']


class EmailOTPSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = EmailOTP
        fields = ['id', 'user', 'otp', 'create_date_time', 'validate_date_time']
