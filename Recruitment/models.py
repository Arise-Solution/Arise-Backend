from django.contrib.auth.models import User
from Authentication.models import MessageOTP
from django.db import models
from django.core.validators import FileExtensionValidator


def path_based_on_user_id_profile_photo(instance, filename):
    return 'profile_photo/{0}/{1}'.format(instance.user.id, filename)


def path_based_on_user_id_resume(instance, filename):
    return 'resume/{0}/{1}'.format(instance.user.id, filename)


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone = models.ForeignKey(MessageOTP, on_delete=models.CASCADE)
    address = models.TextField()
    profile_photo = models.ImageField(upload_to=path_based_on_user_id_profile_photo,
                                      validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])])
    profile_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email


class Resume(models.Model):
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE)
    resume_file = models.FileField(upload_to=path_based_on_user_id_resume,
                                   validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx'])])

    def __str__(self):
        return self.profile.user.email


class Job(models.Model):
    job_title = models.CharField(max_length=255)
    job_description = models.TextField()
    job_company = models.CharField(max_length=128)
    job_experience_choices = (
        ('0-2 years', '0-2 years'),
        ('2-5 years', '2-5 years'),
        ('5-10 years', '5-10 years'),
        ('10+ years', '10+ years')
    )
    job_experience = models.CharField(max_length=10, choices=job_experience_choices)
    job_location = models.CharField(max_length=255)
    job_salary = models.FloatField()
    job_type_choices = (
        ('Full Time', 'Full Time'),
        ('Part Time', 'Part Time'),
        ('Contract', 'Contract'),
        ('Internship', 'Internship'),
    )
    job_type = models.CharField(max_length=20, choices=job_type_choices)
    remote_job = models.BooleanField(default=False)
    job_verified = models.BooleanField(default=False)
    job_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.job_title


class JobApplication(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    cover_letter = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.email
