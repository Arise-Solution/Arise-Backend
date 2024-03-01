from django.urls import path
from .views import (ProfileView, ResumeView, CompanyView, JobView, JobApplicationView, JobCompanyView,
                    FilterView)

urlpatterns = [
    path('profile/', ProfileView.as_view(), name='profile'),
    path('resume/', ResumeView.as_view(), name='resume'),
    path('company/', CompanyView.as_view(), name='company'),
    path('job/', JobView.as_view(), name='job'),
    path('job-application/', JobApplicationView.as_view(), name='job-application'),
    path('job-company/', JobCompanyView.as_view(), name='job-company'),
    path('filter/', FilterView.as_view(), name='filter'),
]
