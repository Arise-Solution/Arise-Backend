from django.contrib import admin
from .models import Profile, Resume, Job, JobApplication


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'profile_completed')


class ResumeAdmin(admin.ModelAdmin):
    list_display = ('profile',)


class JobAdmin(admin.ModelAdmin):
    list_display = ('job_title', 'job_company', 'created_at')


class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('job', 'user')


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Resume, ResumeAdmin)
admin.site.register(Job, JobAdmin)
admin.site.register(JobApplication, JobApplicationAdmin)
