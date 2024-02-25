from django.urls import path
from .views import ProfileView, ResumeView, CompanyView, JobView, JobApplicationView

urlpatterns = [
    path('profile/', ProfileView.as_view(), name='profile'),
    path('resume/', ResumeView.as_view(), name='resume'),
    path('company/', CompanyView.as_view(), name='company'),
    path('job/', JobView.as_view(), name='job'),
    path('job-application/', JobApplicationView.as_view(), name='job-application'),
]
