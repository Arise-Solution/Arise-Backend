from django.urls import path
from .views import ProfileView, ResumeView, JobView, JobApplicationView, FilterView

urlpatterns = [
    path('profile/', ProfileView.as_view(), name='profile'),
    path('resume/', ResumeView.as_view(), name='resume'),
    path('job/', JobView.as_view(), name='job'),
    path('job-application/', JobApplicationView.as_view(), name='job-application'),
    path('filter/', FilterView.as_view(), name='filter'),
]
