from django.http import JsonResponse
import json
from django.forms.models import model_to_dict
from .models import Module, Course, Enrollment, Component
from staff.models import Staff
from sdp.utilities import *
import os

base_upload_path = './uploads/'


# helper function to check if course with courseCode exists
def get_course(course_code):
    courses = Course.objects.all().filter(courseCode=course_code)
    if courses.count() > 0:
        return courses[0]
    return None


# Create your views here.

def index(request):
    try:
        if request.method == 'GET':
            courses = []
            course_set = Course.objects.all();
            if course_set.count() > 0:
                for course in course_set:
                    courses.append(model_to_dict(course))
            return JsonResponse({"all_courses": courses})
        else:
            return JsonResponse(ERR_GET_EXPECTED)
    except Exception as e:
        print(e)
        return JsonResponse(ERR_INTERNAL_ERROR)


def addCourse(request):
    # check if post request
    # post data must contain courseCode, instructor(id), category, isPublished, title, description
    if request.method == 'POST':
        try:
            # get request body and decode
            decoded_body = request.body.decode('utf-8')
            post_data = json.loads(decoded_body)

            # check for presence of all fields
            if not all_fields_present(post_data, ['courseCode', 'instructor', 'category', 'isPublished',
                                                  'title', 'description']):
                return JsonResponse(ERR_REQUIRED_FIELD_ABS)

            course_code = post_data['courseCode']
            # return failure if course already exists or if instructor does not exist
            course = get_course(course_code)
            if course:
                return_data = {"failure": True, 'message': 'Course already exists'}
            else:
                # check if staff with the id exists
                staff = Staff.objects.filter(id=post_data['instructor'])
                if staff.count() == 0:
                    return_data = ERR_STAFF_DOES_NOT_EXIST
                else:
                    # check if instructor permission assigned
                    if staff[0].instructor_set.count() == 0:
                        return_data = ERR_NO_INSTRUCTOR_PERMISSION
                    else:
                        return_data = staff[0].course_set.create(courseCode=course_code,
                                                                 category=post_data['category'],
                                                                 isPublished=post_data['isPublished'],
                                                                 title=post_data['title'],
                                                                 description=post_data['description'])
                        # convert model to dict
                        return_data = model_to_dict(return_data)
        except Exception as e:
            # unknown exception
            print(e)
            return_data = ERR_INTERNAL_ERROR

        # return json response
        return JsonResponse(return_data, safe=False)
    else:
        return JsonResponse(ERR_POST_EXPECTED)


def courseDescription(request, course_code):
    # get course associated. Return failure if none. Else return the course
    try:
        course = get_course(course_code)
        if not course:
            return_data = ERR_COURSE_DOES_NOT_EXIST
        else:
            return_data = model_to_dict(course)  # general course data outer body
            instructor_info = {"username": course.instructor.username}
            return_data['instructor_info'] = instructor_info
            module_data = []  # will contain the list of modules
            module_set = course.module_set
            return_data['module_count'] = module_set.count()
            for module in module_set.all():  # for each module get the list of components
                module_dict = model_to_dict(module)
                component_set = module.component_set
                module_dict['component_count'] = component_set.count()
                components = []
                for component in component_set.all():
                    components.append(model_to_dict(component))
                module_dict['components'] = components
                module_data.append(module_dict)  # append module info to module data list
            return_data['modules'] = module_data  # list of all modules for the course
    except Exception as e:
        print(e)
        return_data = ERR_INTERNAL_ERROR
    return JsonResponse(return_data)


def publishCourse(request, course_code):
    # get course associated, return err if does not exist. Set isPublished and save
    # return updated course
    if request.method == 'POST':
        try:
            course = get_course(course_code)
            if not course:
                return_data = ERR_COURSE_DOES_NOT_EXIST
            else:
                if not course.isPublished:
                    course.isPublished = True
                    course.save()
                    return_data = model_to_dict(course)
        except Exception as e:
            print(e)
            return_data = ERR_INTERNAL_ERROR
    else:
        return_data = ERR_POST_EXPECTED
    return JsonResponse(return_data)


def addModule(request, course_code):
    # post data must have moduleTitle, sequenceNumber
    try:
        course = get_course(course_code)
        if not course:
            return_data = ERR_COURSE_DOES_NOT_EXIST
        else:
            post_data = json.loads(request.body.decode('utf-8'))  # get the post data

            # check all fields present
            if not all_fields_present(post_data, ['moduleTitle', 'sequenceNumber']):
                return JsonResponse(ERR_REQUIRED_FIELD_ABS)

            # make sure there is no module with the sequence number specified
            already_exist_mod_seq = course.module_set.filter(sequenceNumber=post_data['sequenceNumber']).count() > 0
            if already_exist_mod_seq:
                return JsonResponse(ERR_MOD_ORDER_EXISTS)

            module = course.module_set.create(moduleTitle=post_data['moduleTitle'],
                                              sequenceNumber=post_data['sequenceNumber'])
            return_data = model_to_dict(module)  # create module and set the return_data to new module created
    except Exception as e:
        print(e)
        return_data = ERR_INTERNAL_ERROR
    return JsonResponse(return_data)  # ask AK what to return


def update_module_order(request, course_code):
    # POST data must contain module_sequences attribute
    # module_sequences is an array of objects, each with id (module's id) and sequenceNumber
    # frontend check must be performed to ensure there are no modules with duplicate sequenceNumber

    post_data = json.loads(request.body.decode('utf-8'))
    updated = []
    if not all_fields_present(post_data, ['module_sequences']):
        return_data = ERR_REQUIRED_FIELD_ABS
    else:
        course = get_course(course_code)
        if not course:
            return_data = ERR_COURSE_DOES_NOT_EXIST
        else:
            for obj in post_data['module_sequences']:
                module = course.module_set.filter(id=obj.id)[0]  # assumption: you will pass in the right module id
                if module.count() > 0:
                    module = module[0]
                    module.sequenceNumber = obj.sequencNumber
                    module.save()
                    updated.append(model_to_dict(module))
            return_data = {'updated_modules': updated}

    return JsonResponse(return_data)


def update_component_order(request, course_code, module_seq):
    # POST data must contain component_sequences attribute
    # component_sequences is an array of objects, each with id (module's id) and order
    # frontend check must be performed to ensure there are no component with duplicate order

    post_data = json.loads(request.body.decode('utf-8'))
    updated = []
    if not all_fields_present(post_data, ['component_sequences']):
        return_data = ERR_REQUIRED_FIELD_ABS
    else:
        course = get_course(course_code)
        if not course:
            return_data = ERR_COURSE_DOES_NOT_EXIST
        else:
            module = course.module_set.filter(id=module_seq)
            if module.count() == 0:
                return_data = ERR_MOD_DOES_NOT_EXIST
            else:
                module = module[0]  # get the first element
                for obj in post_data['component_sequences']:
                    component = module.component_set.filter(id=obj.id)[0]
                    if component.count() > 0:
                        component = component[0]
                        component.order = obj.order
                        component.save()
                        updated.append(model_to_dict(component))
                return_data = {'updated_components': updated}

    return JsonResponse(return_data)


def addComponent(request, course_code, module_seq):
    module_seq = int(module_seq)
    # POST data must contain order, contentType, content, contentTitle
    try:
        # get the post data
        post_data = json.loads(request.body.decode('utf-8'))

        if not all_fields_present(post_data, ['order', 'contentType', 'content', 'contentTitle']):
            return JsonResponse(ERR_REQUIRED_FIELD_ABS)

        course = get_course(course_code)  # get the course associated, return failure if none
        if not course:
            return_data = ERR_COURSE_DOES_NOT_EXIST
        else:
            # get the module with the sequence number
            if module_seq > course.module_set.count():
                return_data = ERR_MOD_DOES_NOT_EXIST
            else:
                # add component and return newly created component
                module = course.module_set.filter(sequenceNumber=module_seq)[0]

                # return failure if same order already exists
                if module.component_set.filter(order=post_data['order']).count() > 0:
                    return JsonResponse(ERR_COMP_ORDER_EXISTS)

                component = module.component_set.create(order=post_data['order'],
                                                        contentType=post_data['contentType'],
                                                        content=post_data['content'],
                                                        contentTitle=post_data['contentTitle'])
                if component:
                    return_data = model_to_dict(component)
                else:
                    return_data = {'failure': True, 'message': 'Component could not be created'}
    except Exception as e:
        print(e)
        return_data = ERR_INTERNAL_ERROR
    return JsonResponse(return_data)


def enroll(request, course_code):
    # get participant and course associated. Return failure if either does not exist
    # Otherwise create enrollment and return newly created enrollment record
    # POST data must contain staff_id

    try:
        post_data = json.loads(request.body.decode('utf-8'))

        if not all_fields_present(post_data, ['staff_id']):
            return JsonResponse(ERR_REQUIRED_FIELD_ABS)

        course = get_course(course_code)
        staff_id = int(post_data['staff_id'])
        staff = Staff.objects.filter(id=staff_id)  # get participant id from post data

        if not course:
            return_data = ERR_COURSE_DOES_NOT_EXIST
        elif staff.count() == 0:
            return_data = ERR_STAFF_DOES_NOT_EXIST
        elif not course.isPublished:
            return_data = ERR_COURSE_NOT_PUBLISHED  # check if course published
        elif Enrollment.objects.filter(participant_id=staff_id, isCompleted=False).count() > 0:
            # already in one course
            if Enrollment.objects.filter(participant_id=staff_id)[0].course.courseCode == course.courseCode:
                return_data = ERR_ALREADY_ENROLLED_CURR
            else:
                return_data = ERR_ALREADY_ENROLLED_ONE
        elif staff_id == course.instructor.id:
            # cannot enroll in the same course created
            return_data = ERR_PARTICIPANT_INSTRUCT_SAME
        else:
            enrollment = Enrollment()
            enrollment.course = course
            enrollment.participant = staff[0]
            enrollment.save()
            return_data = model_to_dict(enrollment)
    except Exception as e:
        print(e)
        return_data = ERR_INTERNAL_ERROR
    return JsonResponse(return_data)


def get_enrolled_participants(request, course_code):
    try:
        course = get_course(course_code)
        if not course:
            return_data = ERR_COURSE_DOES_NOT_EXIST
        else:
            enrollments = Enrollment.objects.filter(course__courseCode=course_code)
            all_enrolls = []
            for enrollment in enrollments:
                participant = Staff.objects.get(id=enrollment.participant.id)
                enrollment = model_to_dict(enrollment)
                enrollment['participant_info'] = {'username': participant.username}
                all_enrolls.append(enrollment)
            return_data = {'all_enrolls': all_enrolls}
    except Exception as e:
        print(e)
        return_data = ERR_INTERNAL_ERROR
    return JsonResponse(return_data)


def get_completed_participants(request, course_code):
    try:
        course = get_course(course_code)
        if not course:
            return_data = ERR_COURSE_DOES_NOT_EXIST
        else:
            enrollments = Enrollment.objects.filter(course__courseCode=course_code, isCompleted=True)
            completed_enrolls = []
            for enrollment in enrollments:
                participant = Staff.objects.get(id=enrollment.participant.id)
                enrollment = model_to_dict(enrollment)
                enrollment['participant_info'] = {'username': participant.username}
                completed_enrolls.append(enrollment)
            return_data = {'completed_enrolls': completed_enrolls}
    except Exception as e:
        print(e)
        return_data = ERR_INTERNAL_ERROR
    return JsonResponse(return_data)


def upload_component(request, course_code, module_seq):
    if request.method == 'POST':
        path = base_upload_path + str(course_code) + '/' + str(module_seq) + '/' + request.FILES['upload'].name
        f = request.FILES['upload']
        destination = open(path, 'wb+')
        for chunk in f.chunks():
            destination.write(chunk)
        destination.close()
        return_data = {'success': True, 'file_path': path}
    else:
        return_data = ERR_POST_EXPECTED
    return JsonResponse(return_data)


def remove_component(request):
    if request.method == 'POST':
        post_data = json.loads(request.body.decode('utf-8'))
        if not all_fields_present(post_data, ['courseCode', 'module_seq', 'filename']):
            return_data = ERR_REQUIRED_FIELD_ABS
        else:
            path = base_upload_path + post_data['courseCode'] + '/' + post_data['module_seq'] + '/' + post_data[
                'filename']
            os.remove(path)
            return_data = {'success': True}
    return JsonResponse(return_data)


def update_course_progress(request):
    if request.method == 'POST':
        post_data = json.loads(request.body.decode('utf-8'))
        if not all_fields_present(post_data, ['courseCode', 'module_seq', 'filename']):
            return_data = ERR_REQUIRED_FIELD_ABS
        else:
            path = base_upload_path + post_data['courseCode'] + '/' + post_data['module_seq'] + '/' + post_data[
                'filename']
            os.remove(path)
            return_data = {'success': True}
    return JsonResponse(return_data)