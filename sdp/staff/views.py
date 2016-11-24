from django.http import JsonResponse
from django.forms.models import model_to_dict
from .models import Staff, Instructor, Participant
from sdp.utilities import *
import json


def all_instructors(request):
    instructors = []
    for staff in Staff.objects.all():
        if staff.instructor_set.all().count() > 0:
            data = {'username': staff.username, 'id': staff.id}
            instructors.append(data)
    return JsonResponse({'all_instructors': instructors})


def all_participants(request):
    participants = []
    for staff in Staff.objects.all():
        if staff.participant_set.all().count() > 0:
            data = {'username': staff.username, 'id': staff.id}
            participants.append(data)
    return JsonResponse({'all_participants': participants})


def create_staff(request):
    try:
        if request.method == 'POST':
            post_data = json.loads(request.body.decode('utf-8'))
            if not all_fields_present(post_data, ['username', 'password']):
                return_data = ERR_REQUIRED_FIELD_ABS
            else:
                s = Staff(username=post_data['username'], password=post_data['password'])
                s.save()
                return_data = model_to_dict(s)
        else:
            return_data = ERR_POST_EXPECTED
    except Exception as e:
        print(e)
        return_data = ERR_INTERNAL_ERROR
    return JsonResponse(return_data)


def assign_instructor_permission(request):
    # POST data must have username
    try:
        if request.method == 'POST':
            post_data = json.loads(request.body.decode('utf-8'))
            if not all_fields_present(post_data, ['username']):
                return_data = ERR_REQUIRED_FIELD_ABS
            else:
                staff = Staff.objects.filter(username=post_data['username'])
                if staff.count() == 0:
                    return_data = ERR_STAFF_DOES_NOT_EXIST
                else:
                    staff = staff[0]
                    instructor = Instructor()
                    instructor.staff = staff
                    instructor.save()
                    return_data = model_to_dict(staff)
        else:
            return_data = ERR_POST_EXPECTED
    except Exception as e:
        print(e)
        return_data = ERR_INTERNAL_ERROR
    return JsonResponse(return_data)
