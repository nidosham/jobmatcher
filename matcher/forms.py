from django import forms
from .models import *

# loginForm


class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'username'}))
    password = forms.CharField(label='Password', max_length=100,
                               widget=forms.TextInput(attrs={'class': 'form-control',   'type': 'password'}))

# forms.ModelMultipleChoiceField(queryset=Author.objects.all())


class RegistrationForm(forms.Form):
    firstname = forms.CharField(label='firstname', max_length=100,
                                widget=forms.TextInput(attrs={'class': 'form-control',  'id': 'firstname'}))
    lastname = forms.CharField(label='lastname', max_length=100,
                               widget=forms.TextInput(attrs={'class': 'form-control',  'id': 'lastname'}))

    username = forms.CharField(label='Username', max_length=100,
                               widget=forms.TextInput(attrs={'class': 'form-control',  'id': 'username'}))

    email = forms.CharField(label='Email', max_length=100,
                            widget=forms.TextInput(attrs={'class': 'form-control',  id: 'email'}))
    password = forms.CharField(label='Password', max_length=100,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'password', 'onkeyup': "return passwordChanged();"}))
    confirmPassword = forms.CharField(label='Password', max_length=100,
                                      widget=forms.TextInput(attrs={'class': 'form-control',   'type': 'password',  'onkeyup': "return passwordMatch();"}))
    city = forms.CharField(label='City', max_length=100,
                           widget=forms.TextInput(attrs={'class': 'form-control',  'id': 'city'}))
    state = forms.CharField(label='State', max_length=100,
                            widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'state'}))
    country = forms.CharField(label='Country', max_length=100,
                              widget=forms.TextInput(attrs={'class': 'form-control',  'id': 'country'}))


class CourseForm(forms.Form):
    courseName = forms.CharField(label='Course Name', max_length=100, widget=forms.TextInput(
        attrs={'class': 'form-control', 'name': 'school', 'id': 'school'}))
    level = forms.CharField(label='Level of Study', max_length=100, widget=forms.TextInput(
        attrs={'class': 'form-control', 'name': 'level', 'id': 'level'}))
    year_of_study = forms.CharField(label='Years of Study', max_length=100, widget=forms.TextInput(
        attrs={'class': 'form-control', 'name': 'years', 'id': 'years'}))


class EducationForm(forms.Form):
    schoolName = forms.CharField(label='School', max_length=100,
                                 widget=forms.TextInput(attrs={'class': 'form-control',  'id': 'school'}))
    course = forms.ModelMultipleChoiceField(queryset=Course.objects.all())
    #forms.CharField(label='Course', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'course'}))
    field_of_study = forms.CharField(label='Field of study', max_length=100,
                                     widget=forms.TextInput(attrs={'class': 'form-control',  'id': 'field_of_study'}))
    educationLevel = forms.ChoiceField(
        choices=((1, "High School"), (2, "Bachelor"), (3, "Masters"), (4, "PHD")))

# Experience part of form


class ExperienceForm(forms.Form):
    title = forms.CharField(label='Title', max_length=100,
                            widget=forms.TextInput(attrs={'class': 'form-control',  'id': 'title'}))
    employmentType = forms.CharField(label='Employment Type', max_length=100,
                                     widget=forms.TextInput(attrs={'class': 'form-control',  'id': 'type'}))
    fieldofwork = forms.CharField(label='Field of work', max_length=100,
                                  widget=forms.TextInput(attrs={'class': 'form-control',  'id': 'work'}))
    company = forms.CharField(label='Organization/Company', max_length=100,
                              widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'org'}))
    duration = forms.CharField(label='Duration', max_length=100,
                               widget=forms.TextInput(attrs={'class': 'form-control',  'id': 'duration'}))
    country = forms.CharField(label='Country', max_length=100,
                              widget=forms.TextInput(attrs={'class': 'form-control',  'id': 'coutry'}))
    state = forms.CharField(label='State', max_length=100,
                            widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'state'}))
    city = forms.CharField(label='City', max_length=100,
                           widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'city'}))
