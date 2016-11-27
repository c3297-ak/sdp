from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.shortcuts import render
from .models import Staff, Instructor, Participant, Administrator, HumanResource
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

def all_administrators(request):
    administrator = []
    for staff in Staff.objects.all():
        if staff.administrator_set.all().count() > 0:
            data = {'username': staff.username, 'id': staff.id}
            administrator.append(data)
    return JsonResponse({'all_administrators': administrator})

def all_humanResources(request):
    humanResources = []
    for staff in Staff.objects.all():
        if staff.humanresource_set.all().count() > 0:
            data = {'username': staff.username, 'id': staff.id}
            humanResources.append(data)
    return JsonResponse({'all_humanResources': humanResources})

def assign_instructor_permission(request):
    # POST data must have username
    try:
        if request.method == 'POST':
            post_data = json.loads(request.body.decode('utf-8'))
            if not all_fields_present(post_data, ['username']):
                return_data = ERR_REQUIRED_FIELD_ABS
            else:
                # Sourav - add logic for already existing instructor permission
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

def assign_admin_permission(request):
    # POST data must have username
    try:
        if request.method == 'POST':
            post_data = json.loads(request.body.decode('utf-8'))
            if not all_fields_present(post_data, ['username']):
                return_data = ERR_REQUIRED_FIELD_ABS
            else:
                # Sourav - add logic for already existing admin permission
                staff = Staff.objects.filter(username=post_data['username'])
                if staff.count() == 0:
                    return_data = ERR_STAFF_DOES_NOT_EXIST
                else:
                    staff = staff[0]
                    admin = Administrator()
                    admin.staff = staff
                    admin.save()
                    return_data = model_to_dict(staff)
        else:
            return_data = ERR_POST_EXPECTED
    except Exception as e:
        print(e)
        return_data = ERR_INTERNAL_ERROR
    return JsonResponse(return_data)

def assign_hr_permission(request):
    # POST data must have username
    try:
        if request.method == 'POST':
            post_data = json.loads(request.body.decode('utf-8'))
            if not all_fields_present(post_data, ['username']):
                return_data = ERR_REQUIRED_FIELD_ABS
            else:
                # Sourav - add logic for already existing admin permission
                staff = Staff.objects.filter(username=post_data['username'])
                if staff.count() == 0:
                    return_data = ERR_STAFF_DOES_NOT_EXIST
                else:
                    staff = staff[0]
                    hr = HumanResource()
                    hr.staff = staff
                    hr.save()
                    return_data = model_to_dict(staff)
        else:
            return_data = ERR_POST_EXPECTED
    except Exception as e:
        print(e)
        return_data = ERR_INTERNAL_ERROR
    return JsonResponse(return_data)

def login(request):
    if request.method == 'POST':
        try:
            decoded_body = request.body.decode('utf-8')
            post_data = json.loads(decoded_body)

            staff = Staff.objects.all().filter(username=post_data['username'], password=post_data['password'])
            if staff.count() > 0:
                return_data = {'staffId':staff[0].id}
            else:
                return_data = ERR_STAFF_DOES_NOT_EXIST
        except Exception as e:
            print(e)
            return_data = ERR_INTERNAL_ERROR
    else:
        return_data = ERR_POST_EXPECTED
    return JsonResponse(return_data)

def register(request):
    try:
        if request.method == 'POST':
            post_data = json.loads(request.body.decode('utf-8'))
            if not all_fields_present(post_data, ['username', 'password']):
                return_data = ERR_REQUIRED_FIELD_ABS
            else:
                staff = Staff.objects.all().filter(username=post_data['username'])
                if staff.count() > 0:
                    return_data = ERR_STAFF_ALREADY_EXIST
                else:
                    newStaff = Staff(
                        username = post_data['username'],
                        password = post_data['password'])
                    newStaff.save()
                    # NOTE: add participant permisson
                    participant = Participant()
                    participant.staff = newStaff
                    participant.save()
                    return_data = model_to_dict(newStaff)
        else:
            return_data = ERR_POST_EXPECTED
    except Exception as e:
        print(e)
        return_data = ERR_INTERNAL_ERROR
    return JsonResponse(return_data)

def loginPage(request):
    return render(request, 'staff/loginPage.html')

def home(request):
    return render(request, 'staff/home.html')

def participant(request):
    return render(request, 'staff/participant.html')

def instructor(request):
    return render(request, 'staff/instructor.html')

def administrator(request):
    return render(request, 'staff/admin.html')

def hr(request):
    return render(request, 'staff/hr.html')