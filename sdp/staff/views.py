from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.shortcuts import render
from .models import Staff, Instructor, Participant, Administrator, HumanResource
from courses.models import Enrollment, Course
from sdp.utilities import *
import json

def courseCompleted (request, staff_username):
    try:
        if request.method == 'GET':
            staff = Staff.objects.filter(username=staff_username)
            if staff.count() == 0:
                return_data = ERR_STAFF_DOES_NOT_EXIST
            staff = staff[0]

            completed_enrolls = []
            enrollments = Enrollment.objects.filter(isCompleted=True, participant=staff)
            for enrollment in enrollments:
                course = model_to_dict(enrollment.course)
                completed_enrolls.append(course)
            return_data = {'completed_enrolls': completed_enrolls}
            
        else:
            return_data = ERR_GET_EXPECTED
    except Exception as e:
        print(e)
        return_data = ERR_INTERNAL_ERROR
    return JsonResponse(return_data)

def staffs(request):
    try:
        if request.method == 'GET':
            staffs = []
            for staff in Staff.objects.all():
                staffs.append(staff.username)
            return JsonResponse({'staffs': staffs})
        else:
            return_data = ERR_GET_EXPECTED
    except Exception as e:
        print(e)
        return_data = ERR_INTERNAL_ERROR
    return JsonResponse(return_data)

def getStaffUsername(request, staff_id):
    try:
        if request.method == 'GET':
            staff = Staff.objects.filter(id=staff_id)
            if staff.count() == 0:
                return_data = ERR_STAFF_DOES_NOT_EXIST
            else:
                username = staff[0].username;
            return JsonResponse({
                'username': username
            })
        else:
            return_data = ERR_POST_EXPECTED
    except Exception as e:
        print(e)
        return_data = ERR_INTERNAL_ERROR
    return JsonResponse(return_data)

def staffInfo(request, staff_username):
    try:
        if request.method == 'GET':
            username = ""
            isInstructor = False
            isAdmin = False
            isHR = False

            staff = Staff.objects.filter(username=staff_username)
            if staff.count() == 0:
                return_data = ERR_STAFF_DOES_NOT_EXIST
            else:
                username = staff[0].username;
               
            staff = staff[0]
            
            if staff.instructor_set.all().count() > 0:
                isInstructor = True

            if staff.administrator_set.all().count() > 0:
                isAdmin = True

            if staff.humanresource_set.all().count() > 0:
                isHR = True

            return JsonResponse({
                'username': username,
                'participant': True,
                'instructor': isInstructor,
                'admin': isAdmin,
                'hr': isHR
            })
        else:
            return_data = ERR_POST_EXPECTED
    except Exception as e:
        print(e)
        return_data = ERR_INTERNAL_ERROR
    return JsonResponse(return_data)

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
                staff = Staff.objects.filter(username=post_data['username'])
                if staff.count() == 0:
                    return_data = ERR_STAFF_DOES_NOT_EXIST
                else:
                    if staff[0].instructor_set.count() == 0:
                        staff = staff[0]
                        instructor = Instructor()
                        instructor.staff = staff
                        instructor.save()
                        return_data = model_to_dict(staff)
                    else:
                        return_data = ERR_PERMISSION_EXIST
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
                    if staff[0].administrator_set.count() == 0:
                        staff = staff[0]
                        admin = Administrator()
                        admin.staff = staff
                        admin.save()
                        return_data = model_to_dict(staff)
                    else:
                        return_data = ERR_PERMISSION_EXIST
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
                    if staff[0].humanresource_set.count() == 0:
                        staff = staff[0]
                        hr = HumanResource()
                        hr.staff = staff
                        hr.save()
                        return_data = model_to_dict(staff)
                    else:
                        return_data = ERR_PERMISSION_EXIST
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

            staff = Staff.objects.all().filter(username=post_data['username'])
            if staff.count() > 0:
                staff = staff[0]
                if staff.password == post_data['password']:
                    return_data = dict()
                    return_data['staffId'] = staff.id
                    return_data['participant'] = True  # default
                    # check if instructor
                    if staff.instructor_set.count() > 0:
                        return_data['instructor'] = True
                    if staff.administrator_set.count() > 0:
                        return_data['administrator'] = True
                    if staff.humanresource_set.count() > 0:
                        return_data['human_resource'] = True
                else:
                    return_data = ERR_STAFF_INCORRECT_PASSWORD
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
                        username=post_data['username'],
                        password=post_data['password'])
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

def enrolled_courses(request, staff_id):
    # return {'course_list': [{'courseCode': xxx, 'title': xxx, 'progress': xyz},...]}
    # or an appropriate error message
    try:
        if request.method == 'GET':
            staff = Staff.objects.filter(pk=staff_id)
            if staff.count() > 0:
                staff = staff[0]
                return_data = dict()
                courses = []
                for enrollment in Enrollment.objects.filter(participant=staff):
                    data = {'courseCode': enrollment.course.courseCode, 'title': enrollment.course.title,
                            'progress': enrollment.modules_completed, 'isCompleted': enrollment.isCompleted, 'isRetaking' : enrollment.isRetaking}
                    courses.append(data)
                return_data['course_list'] = courses
            else:
                return_data = ERR_STAFF_DOES_NOT_EXIST
        else:
            return_data = ERR_GET_EXPECTED
    except Exception as e:
        print(e)
        return_data = ERR_INTERNAL_ERROR
    return JsonResponse(return_data)

def courselist_instructor(request, staff_id):
    # returns {'course_list' : [{'courseCode': xyz, 'title': xyz}...]}
    # or an appropriate error message
    try:
        if request.method == 'GET':
            staff = Staff.objects.filter(pk=staff_id)
            if staff.count() > 0:
                staff = staff[0]
                # No instructor permission assigned
                if staff.instructor_set.count() == 0:
                    return JsonResponse(ERR_NO_INSTRUCTOR_PERMISSION)

                return_data = dict()
                courses = []
                for course in Course.objects.filter(instructor=staff):
                    data = {'courseCode': course.courseCode, 'title': course.title, 'isPublished': course.isPublished, 'category': course.category.name, 'description':course.description}
                    courses.append(data)
                return_data['course_list'] = courses
            else:
                return_data = ERR_STAFF_DOES_NOT_EXIST
        else:
            return_data = ERR_GET_EXPECTED
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