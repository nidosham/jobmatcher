from . import views
from django.urls import path, include
urlpatterns = [
    path('registration', views.registration, name='registration'),
    path('settings', views.settings, name='settings'),
    path('home', views.home, name='home'),
    path('login', views.login, name='login'),
    path('', views.index, name='index'),
    path('about', views.about, name='about'),
    path('profile', views.profile, name='profile'),
    path('qualifications', views.qualifications, name="qualifications"),
    path('education', views.addEducation, name="education"),
    path('experience', views.addExperience, name="experience"),
    path('skills', views.addSkills, name="skills"),
    path('experience/<int:id>', views.editExperience, name="editExperience"),
    path('education/<int:id>', views.editEducation, name="editEducation"),
    path('contacts', views.contacts, name="contacts"),
    path('notifications', views.notifications, name="notifications"),
    path('appliedjobs', views.appliedJobs, name="appliedjobs"),
    path('logout', views.logout, name="logout"),
]
