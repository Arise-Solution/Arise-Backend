from django.contrib import admin
from .models import Profile, Resume, Company, Job, JobApplication

admin.site.register(Profile)
admin.site.register(Resume)
admin.site.register(Company)
admin.site.register(Job)
admin.site.register(JobApplication)
