from django.urls import path
from .views import (MessageOTPSend, MessageOTPVerify, MessageOTPResend, EmailOTPSend, EmailOTPVerify,
                    EmailOTPResend, SignUpView, LoginView, LogoutView)

urlpatterns = [
    path('message/send/', MessageOTPSend.as_view(), name='message-send'),
    path('message/verify/', MessageOTPVerify.as_view(), name='message-verify'),
    path('message/resend/', MessageOTPResend.as_view(), name='message-resend'),
    path('email/send/', EmailOTPSend.as_view(), name='email-send'),
    path('email/verify/', EmailOTPVerify.as_view(), name='email-verify'),
    path('email/resend/', EmailOTPResend.as_view(), name='email-resend'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
