from django.conf.urls import url, include
from . import views

app_name = 'staff'

urlpatterns = [

    url(r'^(?P<staff_username>.+)/staffInfo$', views.staffInfo, name='staffInfo'),
    url(r'^(?P<staff_username>.+)/courseCompleted$', views.courseCompleted, name='courseCompleted'),
    url(r'^(?P<staff_id>[0-9]+)/getStaffUsername$', views.getStaffUsername, name='getStaffUsername'),
    url(r'^staffs$', views.staffs, name='staffs'),

    # staff/instructors
    url(r'^instructors$', views.all_instructors, name='all_instructors'),
    # staff/participants
    url(r'^participants$', views.all_participants, name='all_participant'),
    # staff/humanResources
    url(r'^humanResources$', views.all_humanResources, name='all_humanResources'),
    # staff/admins
    url(r'^administrators$', views.all_administrators, name='all_administrators'),

    # staff/assign_instructor
    url(r'^assign_instructor$', views.assign_instructor_permission, name='assign_instructor'),
    # staff/assign_instructor
    url(r'^assign_admin$', views.assign_admin_permission, name='assign_admin'),
    # staff/assign_instructor
    url(r'^assign_hr$', views.assign_hr_permission, name='assign_hr'),

    # staff/login
    url(r'^login$', views.login, name='login'),
    # staff/register
    url(r'^register$', views.register, name='register'),

    # UI endpoints
    url(r'^$', views.loginPage, name='loginPage'),
    url(r'^loginPage$', views.loginPage, name='loginPage'),
    url(r'^home$', views.home, name='home'),
    url(r'^instructor$', views.instructor, name='instructor'),
    url(r'^participant$', views.participant, name='participant'),
    url(r'^hr$', views.hr, name='hr'),
    url(r'^administrator$', views.administrator, name='administrator'),

    # url to get the courses enrolled in by a staff
    url(r'^(?P<staff_id>[0-9]+)/enrolled', views.enrolled_courses, name='enrolled_courses'),

    # url to get the courses created as an instructor by the staff
    url(r'^(?P<staff_id>[0-9]+)/courselist_instructor', views.courselist_instructor, name='courselist_instructor'),
]
