from django.contrib.auth.models import User
from django.db import models


class MessageOTP(models.Model):
    class Meta:
        verbose_name_plural = 'Message OTP'
        get_latest_by = 'create_date_time'
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=False)
    otp = models.CharField(max_length=6, blank=False)
    create_date_time = models.DateTimeField(auto_now_add=True)
    validate_date_time = models.DateTimeField(blank=True)
    object = models.manager

    def __str__(self):
        return str(self.user) + ' -> ' + self.otp


class EmailOTP(models.Model):
    class Meta:
        verbose_name_plural = 'Email OTP'
        get_latest_by = 'create_date_time'
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6, blank=False)
    create_date_time = models.DateTimeField(auto_now_add=True)
    validate_date_time = models.DateTimeField(blank=True)
    object = models.manager

    def __str__(self):
        return str(self.user) + ' -> ' + self.otp
