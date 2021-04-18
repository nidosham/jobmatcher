
from django.utils import timezone
from django.db import models

from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
# Create your models here.
User = get_user_model()
# define a the users of the sites/the job seeker


class Course(models.Model):
    courseName = models.CharField(max_length=20)
    field_of_study = models.CharField(max_length=20)
    level = models.CharField(max_length=20)
    years_of_study = models.CharField(max_length=20)

    def __str__(self):
        return self.courseName


# education level
class Education(models.Model):
    schoolName = models.CharField(max_length=50)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    educationLevel = models.CharField(max_length=50)
    field_of_study = models.CharField(max_length=50)
    person = models.ForeignKey(
        User, related_name='user', on_delete=models.CASCADE)

    def __str__(self):
        return course

# Previous job experience/job tasks


class Experience(models.Model):
    title = models.CharField(max_length=50)
    employmentType = models.CharField(max_length=50)
    fieldOfwork = models.CharField(max_length=50)
    company = models.CharField(max_length=100)
    duration = models.CharField(max_length=20)
    country = models.CharField(max_length=30)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    person = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.primary_key

# User receiving message for jobs collected


class Job(models.Model):
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, default=1)
    job_title = models.CharField(max_length=100)
    link = models.CharField(max_length=255)
    location = models.CharField(max_length=100)
    advertised_date = models.CharField(max_length=50)
    time = models.DateTimeField(
        blank=True, default=timezone.now, max_length=200)

    def __str__(self):
        return self.job_title


class MySkills(models.Model):
    person = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    skill = models.CharField(max_length=50)


class Residence(models.Model):
    person = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    town = models.CharField(max_length=120)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)

    def __str__(self):
        return self.town
