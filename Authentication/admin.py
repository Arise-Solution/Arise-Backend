from django.contrib import admin
from .models import MessageOTP, EmailOTP


class MessageOTPAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone_number', 'otp', 'create_date_time', 'validate_date_time']
    search_fields = ['user', 'phone_number', 'otp', 'create_date_time', 'validate_date_time']
    list_filter = ['user', 'phone_number', 'otp', 'create_date_time', 'validate_date_time']


class EmailOTPAdmin(admin.ModelAdmin):
    list_display = ['user', 'otp', 'create_date_time', 'validate_date_time']
    search_fields = ['user', 'otp', 'create_date_time', 'validate_date_time']
    list_filter = ['user', 'otp', 'create_date_time', 'validate_date_time']


admin.site.register(MessageOTP, MessageOTPAdmin)
admin.site.register(EmailOTP, EmailOTPAdmin)
