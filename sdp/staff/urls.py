from django.conf.urls import url, include
from . import views

app_name = 'staff'

urlpatterns = [
    # staff/create
    url(r'^create', views.create_staff, name='create_staff'),
    # staff/instructor
    url(r'^instructors$', views.all_instructors, name='all_instructors'),
    # staff/assign_instructor
    url(r'^assign_instructor$', views.assign_instructor_permission, name='assign_instructor'),
    # staff/participant
    url(r'^participants$', views.all_participants, name='all_participant')
]
