from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Profile, Resume, Job, JobApplication
from .serializers import (ProfileSerializer, ResumeSerializer,
                          JobSerializer, JobApplicationSerializer)
from django_filters import rest_framework as filters
from .utils import send_job_application_received_email


class ProfileView(LoginRequiredMixin, APIView):
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def get(request, *args, **kwargs):
        profile = Profile.objects.get(user=request.user)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def post(request, *args, **kwargs):
        data = request.data
        serializer = ProfileSerializer(data=data)
        if serializer.is_valid():
            new_profile_photo = request.data.get('profile_photo', None)
            if new_profile_photo:
                max_size = 5 * 1024 * 1024
                if new_profile_photo.size > max_size:
                    return Response({"error": "Profile photo size cannot exceed 5MB."},
                                    status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def put(request, *args, **kwargs):
        profile = Profile.objects.get(user=request.user)
        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            new_profile_photo = request.data.get('profile_photo', None)
            if new_profile_photo:
                max_size = 5 * 1024 * 1024
                if new_profile_photo.size > max_size:
                    return Response({"error": "Profile photo size cannot exceed 5MB."},
                                    status=status.HTTP_400_BAD_REQUEST)
                if profile.profile_photo:
                    profile.profile_photo.delete(save=False)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResumeView(LoginRequiredMixin, APIView):
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def get(request, *args, **kwargs):
        resume = Resume.objects.get(profile__user=request.user)
        serializer = ResumeSerializer(resume)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def post(request, *args, **kwargs):
        data = request.data
        serializer = ResumeSerializer(data=data)
        if serializer.is_valid():
            new_resume = request.data.get('resume', None)
            if new_resume:
                max_size = 2 * 1024 * 1024
                if new_resume.size > max_size:
                    return Response({"error": "Resume size cannot exceed 2MB."},
                                    status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def put(request, *args, **kwargs):
        resume = Resume.objects.get(profile__user=request.user)
        new_resume = request.data.get('resume', None)
        if new_resume and resume.resume:
            resume.resume.delete()
        serializer = ResumeSerializer(resume, data=request.data, partial=True)
        if serializer.is_valid():
            max_size = 2 * 1024 * 1024
            if new_resume and new_resume.size > max_size:
                return Response({"error": "Resume size cannot exceed 2MB."},
                                status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class JobView(LoginRequiredMixin, APIView):
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def get(request, *args, **kwargs):
        jobs = Job.objects.filter(Q(job_type=request.data['job_type']) & Q(job_verified=True))
        serializer = JobSerializer(jobs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class JobApplicationView(LoginRequiredMixin, APIView):
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def get(request, *args, **kwargs):
        if not request.data['viewer']:
            job_applications = JobApplication.objects.filter(job__company__user=request.user)
            serializer = JobApplicationSerializer(job_applications, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        job_applications = JobApplication.objects.filter(user=request.user)
        serializer = JobApplicationSerializer(job_applications)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def post(request, *args, **kwargs):
        data = request.data
        serializer = JobApplicationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            template_data = {
                'applicant_name': request.user.profile.full_name,
                'job_title': serializer.validated_data['job'].job_title,
                'company_name': serializer.validated_data['job'].job_company,
            }
            send_job_application_received_email(request.user.email, template_data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def delete(request, *args, **kwargs):
        job_application = JobApplication.objects.get(user=request.user,
                                                     id=kwargs.get('job_application_id'))
        job_application.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FilterView(LoginRequiredMixin, APIView):
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated,)

    class JobFilter(filters.FilterSet):
        class Meta:
            model = Job
            fields = {
                'job_title': ['exact', 'icontains'],
                'job_experience': ['exact'],
                'job_location': ['exact', 'icontains'],
                'job_salary': ['exact', 'gte', 'lte'],
                'job_type': ['exact'],
                'remote_job': ['exact'],
            }

    def get(self, request, *args, **kwargs):
        filter_data = request.data.get('filter_data', {})
        queryset = Job.objects.all()
        filter_class = self.JobFilter(filter_data, queryset=queryset)
        serializer = JobSerializer(filter_class.qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
