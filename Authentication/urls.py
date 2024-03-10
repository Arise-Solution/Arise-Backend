from django.urls import path
from .views import GoogleLogin, UserRedirectView, MessageOTPSend, MessageOTPVerify, SignupVerificationView

urlpatterns = [
    path('google/', GoogleLogin.as_view(), name='google_login'),
    path("~redirect/", view=UserRedirectView.as_view(), name="redirect"),
    path('message-otp-send/', MessageOTPSend.as_view(), name='message-otp-send'),
    path('message-otp-verify/', MessageOTPVerify.as_view(), name='message-otp-verify'),
    path('signup-verification/', SignupVerificationView.as_view(), name='signup-verification'),
]
