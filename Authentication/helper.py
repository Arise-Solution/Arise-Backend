from django.conf import settings
from django.core.mail import EmailMessage
from twilio.rest import Client


class MessageHandler:
    phone_number = None
    otp = None

    def __init__(self, phone_number, otp) -> None:
        self.phone_number = phone_number
        self.otp = otp

    def send_otp_via_message(self):
        client = Client(settings.ACCOUNT_SID, settings.AUTH_TOKEN)
        client.messages.create(body=f'your otp is:{self.otp}', from_=f'{settings.TWILIO_PHONE_NUMBER}',
                               to=f'{settings.COUNTRY_CODE}{self.phone_number}')


class EmailHandler:
    email = None
    otp = None

    def __init__(self, email, otp) -> None:
        self.email = email
        self.otp = otp

    def send_otp_via_email(self):
        email = EmailMessage(
            subject='OTP',
            body=f'your otp is:{self.otp}',
            from_email=settings.EMAIL_HOST_USER,
            to=[self.email]
        )
        email.send()
