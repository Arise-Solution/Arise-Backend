from django.urls import path
from .views import GoogleLogin, UserRedirectView, MessageOTPSend, MessageOTPVerify

urlpatterns = [
    path('google/', GoogleLogin.as_view(), name='google_login'),
    path("~redirect/", view=UserRedirectView.as_view(), name="redirect"),
    path('message-otp-send/', MessageOTPSend.as_view()),
    path('message-otp-verify/', MessageOTPVerify.as_view()),
]
