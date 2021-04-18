from django.shortcuts import render
from django.utils import timezone
from django.template import RequestContext
from django.shortcuts import get_list_or_404, get_object_or_404
from django.views.decorators.clickjacking import xframe_options_exempt
from django.template.loader import render_to_string
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, get_user_model
from django.urls import reverse
from .forms import *
from django.contrib.sessions.models import Session
from matcher.models import *
import datetime
from matcher.crawler import find_jobs_from
# Create your views here.
User = get_user_model()


@ xframe_options_exempt
def registration(request):
    form = RegistrationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        firstname = form.cleaned_data['firstname']
        lastname = form.cleaned_data['lastname']
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        email = form.cleaned_data['email']
        city = form.cleaned_data['city']
        state = form.cleaned_data['state']
        country = form.cleaned_data['country']

        user = User.objects.create_user(
            username, email, password,
            first_name=firstname,
            last_name=lastname,
        )

        user = User.objects.get(username=username)
        residence = Residence(person=user, town=city,
                              state=state, country=country)
        residence.save()
        # stores the favourite games

        return render(request, 'matcher/registration.html', {'form': form, 'flag': True})

    form = RegistrationForm()
    return render(request, 'matcher/registration.html', {'form': form, 'flag': False})

# show user profile including activities and settings


def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            # process data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            request.session['username'] = username

            if user is not None:
                # request.session.create()
                return HttpResponseRedirect(reverse('home'))

            else:
                # if (request.session.session_key == None):
                return HttpResponse("user is not authenticated")
        else:
            return HttpResponse("form is not valid")
    form = LoginForm()
    return render(request, 'matcher/login.html', {'form': form})


def profile(request):
    if request.session.has_key('username'):
        user = User.objects.get(username=request.session['username'])
        return render(request, "matcher/profile.html")
    else:
        return HttpResponseRedirect(reverse('login'))


def about(request):
    return render(request, 'matcher/aboutus.html')


# Shows the specific message content
def myinbox(request, id):
    message = Job.objects.get(id=id)
    return render(request, 'matcher/themessage.html', {'message': message})


def qualifications(request):
    if request.session.has_key('username'):
        user = User.objects.get(username=request.session['username'])
        form1 = Education.objects.filter(person=user)
        form2 = Experience.objects.filter(person=user)
        return render(request, 'matcher/qualifications.html', {'form1': form1, 'form2': form2})
    else:
        HttpResponseRedirect(reverse('login'))


def addCourse(request):
    if request.session.has_key["username"]:
        user = User.objects.get(username=request.session['username'])
        if request.method == 'POST':
            form = CourseForm(request.POST)
            if form.is_valid():
                courseName = form.cleaned_data['course']
                level = form.cleaned_data['level']
                field_of_study = form.cleaned_data['field']
                years_of_study = form.cleaned_data['years']
                course = Course(courseName, level,
                                field_of_study, years_of_study)
                course.save()
                location = Residence.objects.get(person=user)
                job_list = find_jobs_from("Indeed", course, location,
                                          "titles, date_listed, links", "myjobs")

                for i in range(len(job_list["titles"])):
                    job = Job(receiver=user, job_title=job_list['titles'][i].rstrip(
                        "\nnew"), link=job_list['links'][i], advertised_date=job_list["date_listed"][i])
                    job.save()
                return HttpResponseRedirect(reverse('qualifications'))
    else:
        HttpResponseRedirect(reverse('login'))


def editCourse(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            courseName = form.cleaned_data['course']
            level = form.cleaned_data['level']
            field_of_study = form.cleaned_data['field']
            years_of_study = form.cleaned_data['years']
            course = Course(courseName, level, field_of_study, years_of_study)
            course.save()
            return HttpResponseRedirect(reverse('qualifications'))


def deleteCourse(request, id):
    course = Course.objects.get(id=id)
    course.delete()


def addEducation(request):
    if request.method == 'POST':
        form = EducationForm(request.POST)
        if form.is_valid():
            schoolName = form.cleaned_data["schoolName"]
            course = form.cleaned_data.get("course")
            field_of_study = form.cleaned_data["field_of_study"]
            educationLevel = form.cleaned_data["educationLevel"]
            user = User.objects.get(
                username=request.session['username'])

            st1 = course.__str__()
            k = len(st1)-3
            course_name = st1[20:k]
            print("+++", course_name)
            course = Course.objects.get(courseName=course_name)
            edu = Education(schoolName=schoolName, course=course,
                            educationLevel=educationLevel, field_of_study=field_of_study, person=user)
            edu.save()
            location = Residence.objects.get(person=user)
            job_list = find_jobs_from("Indeed", course, location,
                                      "titles, date_listed, links", "myjobs")
            for i in range(len(job_list["titles"])):
                job = Job(receiver=user, job_title=job_list['titles'][i].rstrip(
                    "\nnew"), link=job_list['links'][i], advertised_date=job_list["date_listed"][i])
                job.save()
            return HttpResponseRedirect(reverse('qualifications'))

    form = EducationForm()
    return render(request, 'matcher/education.html', {'form': form})


def editEducation(request, id):
    if request.method == 'POST':
        form = EducationForm(request.POST)
        if form.is_valid():
            schoolName = form.cleaned_data["schoolName"]
            course = form.cleaned_data.get("course")
            field_of_study = form.cleaned_data["field_of_study"]
            educationLevel = form.cleaned_data["educationLevel"]
            user = User.objects.get(
                username=request.session['username'])

            st1 = course.__str__()
            k = len(st1)-3
            course_name = st1[20:k]
            print("+++", course_name)
            course = Course.objects.get(courseName=course_name)
            edu = Education(schoolName=schoolName, course=course,
                            educationLevel=educationLevel, field_of_study=field_of_study, person=user)
            edu.save()
            return HttpResponseRedirect(reverse('qualifications'))
    form = EducationForm()
    return render(request, 'matcher/education.html', {'form': form})


def deleteEducation(request, id):
    Education.objects.get(id=id).delete()


def contacts(request):
    return render(request, 'matcher/contacts.html')


def settings(request):
    return render(request, 'matcher/settings.html')


def addExperience(request):
    # if request.session.has_key('username'):
    if request.method == 'POST':
        form = ExperienceForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            employmentType = form.cleaned_data["employmentType"]
            fieldOfwork = form.cleaned_data["fieldofwork"]
            company = form.cleaned_data["company"]
            duration = form.cleaned_data["duration"]
            country = form.cleaned_data["country"]
            city = form.cleaned_data["city"]
            state = form.cleaned_data["state"]
            user = User.objects.get(username=request.session['username'])
            # save data
            expe = Experience(title=title, employmentType=employmentType,
                              fieldOfwork=fieldOfwork, company=company, duration=duration, country=country, state=state, city=city, person=user)
            expe.save()
            return HttpResponseRedirect(reverse('qualifications'))

    # generate form inputs for the experince form template
    form = ExperienceForm()
    return render(request, 'matcher/experience.html', {'form': form})


def editExperience(request, id):
   # if request.session.has_key('username'):
    if request.method == 'POST':
        form = ExperienceForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            employmentType = form.cleaned_data["employmentType"]
            fieldOfwork = form.cleaned_data["fieldofwork"]
            company = form.cleaned_data["company"]
            duration = form.cleaned_data["duration"]
            country = form.cleaned_data["country"]
            city = form.cleaned_data["city"]
            state = form.cleaned_data["state"]
            user = User.objects.get(username=request.session['username'])
            # save data
            expe = Experience.objects.filter(player=user)
            expe = Experience(title=title, employmentType=employmentType,
                              fieldOfwork=fieldOfwork, company=company, duration=duration, country=country, state=state, city=city)
            expe.save()
            return HttpResponseRedirect(reverse('qualifications'))

    # generate form inputs for the experince form template
    form = ExperienceForm()
    return render(request, 'matcher/experience.html', {'form': form})


def deleteExperiences(request, id):
    Experience.objects.get(id=id).delete()


def addSkills(request):
    if request.method == "POST":
        if request.is_ajax():
            the_skill = request.POST.get('askill', None)  # getting data
            username = request.session['username']
            cuser = User.objects.get(username=username)
            skill = MySkills(user=cuser, skill=the_skill)
            skill.save()
            response = {
                'msg': the_skill  # response message
            }
            return JsonResponse(responsesafe=False)  # return response as JSON

        else:
            response = {
                'msg': 'Your message has not been sent!'  # response message
            }
            return JsonResponse(response)  # return response as JSON


def deleteSkill(request, id):
    if request.session.has_key('username'):
        MySkills.objects.get(id=id).delete()
    else:
        return HttpResponseRedirect(reverse('login'))


def home(request):
    if request.session.has_key('username'):
        username = request.session['username']
        user = User.objects.get(username=username)
        '''course = Education.objects.get(person=user)
        print("########"+course)
        location = Residence.objects.get(person=user)
        job_list = find_jobs_from("Indeed", "IT", "Arizona",
                                  "titles, date_listed, links", "myjobs")
        for i in range(len(job_list["titles"])):
            job = Job(receiver=user, job_title=job_list['titles'][i].rstrip(
                "\nnew"), link=job_list['links'][i], advertised_date=job_list["date_listed"][i])
            job.save()
            '''
        return render(request, 'matcher/home.html')
    else:
        return HttpResponseRedirect(reverse('login'))


def appliedJobs(request):
    return render(request, 'matcher/appliedjobs.html')


@ xframe_options_exempt
def index(request):
    return render(request, 'matcher/index.html')


def notifications(request):
    uname = request.session['username']
    user = User.objects.get(username=uname)
    jobList = Job.objects.filter(
        receiver=user)
    print("####", user)
    return render(request, 'matcher/notifications.html', {'notificationList': jobList})

# Show faqs page

# function to check existence of the username
# it ensure no two players share the same username


def validate_username(request):
    username = request.GET.get('username', None)
    data = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    return JsonResponse(data)


def logout(request):   # logout function
    del request.session['username']
    return HttpResponseRedirect(reverse('index'))


def delete_account(request, uname):
    User.objects.filter(username=uname).delete()


# def getJobs(request):
