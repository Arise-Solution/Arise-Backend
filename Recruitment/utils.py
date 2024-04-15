from django.core.mail import EmailMessage
from django.template.loader import render_to_string


def send_job_application_received_email(applicant_email, template_data):
    subject = 'Acknowledgment of Job Application'
    message = render_to_string('email_templates/job_application_received.html',
                               {'applicant_name': template_data['applicant_name'],
                                'job_title': template_data['job_title'],
                                'company_name': template_data['company_name']})
    to_email = [applicant_email]
    email = EmailMessage(subject, message, to=to_email)
    email.send()
