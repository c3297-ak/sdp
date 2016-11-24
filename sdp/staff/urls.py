from django.conf.urls import url, include
from . import views

app_name = 'staff'

urlpatterns = [
    # Note: need to add <instructor_id> to allow multiple instructors
    # staff/instructor
    url(r'^instructors$', views.all_instructors, name='all_instructors'),

    # Note: need to add <participant_id> to allow multiple participants
    # staff/participant
    url(r'^participants$', views.all_participants, name='all_participant')
]
