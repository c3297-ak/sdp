from django.http import JsonResponse
import json
from django.forms.models import model_to_dict
from .models import Module, Course, Enrollment, ImageComponent, FileComponent, TextComponent, VideoComponent
from .models import Category
from staff.models import Staff
from sdp.utilities import *
import os
import datetime

from django.shortcuts import render


# --------------------------------------------------- CATEGORIES ----------------------------------------------------


# add a new category to the database
def add_category(request):
    # check if post request
    # post data must contain category_name
    if request.method == 'POST':
        try:
            # get request body and decode
            decoded_body = request.body.decode('utf-8')
            post_data = json.loads(decoded_body)

            # check for presence of all fields
            if not all_fields_present(post_data, ['category_name']):
                return JsonResponse(ERR_REQUIRED_FIELD_ABS)

            category_name = post_data['category_name']
            category = Category.objects.filter(name=category_name)
            if category.count() == 0:
                new_cat = Category(name=category_name)
                new_cat.save()
                return JsonResponse(model_to_dict(new_cat))
            else:
                return JsonResponse(ERR_CATEGORY_ALREADY_EXISTS)
        except Exception as e:
            print(e)
            return JsonResponse(ERR_INTERNAL_ERROR)
    else:
        return JsonResponse(ERR_POST_EXPECTED)


# return all the categories in the database
def get_categories(request):
    return JsonResponse({'all_categories': __get_all_categories()})


def __get_all_categories():
    categories = []
    for category in Category.objects.all():
        categories.append(model_to_dict(category))
    return categories


# remove a particular category from the database
def remove_category(request):
    # check if post request
    # post data must contain category_name
    if request.method == 'POST':
        try:
            # get request body and decode
            decoded_body = request.body.decode('utf-8')
            post_data = json.loads(decoded_body)

            # check for presence of all fields
            if not all_fields_present(post_data, ['category_name']):
                return JsonResponse(ERR_REQUIRED_FIELD_ABS)

            category_name = post_data['category_name']
            category = Category.objects.filter(name=category_name)
            if category.count() == 0:
                return JsonResponse(ERR_CATEGORY_DOES_NOT_EXIST)
            else:
                category[0].delete()
                return JsonResponse({'success': True, 'all_categories': __get_all_categories()})
        except Exception as e:
            print(e)
            return JsonResponse(ERR_INTERNAL_ERROR)
    else:
        return JsonResponse(ERR_POST_EXPECTED)


# --------------------------------------------------- COURSES --------------------------------------------------------


# helper function to check if course with courseCode exists
def get_course(course_code):
    courses = Course.objects.all().filter(courseCode=course_code)
    if courses.count() > 0:
        return courses[0]
    return None


# function to add a course to the database
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
                        category = Category.objects.filter(name=post_data['category'])
                        if category.count() == 0:
                            return JsonResponse(ERR_CATEGORY_DOES_NOT_EXIST)
                        category = category[0]
                        return_data = staff[0].course_set.create(courseCode=course_code,
                                                                 category=category,
                                                                 isPublished=post_data['isPublished'],
                                                                 title=post_data['title'],
                                                                 description=post_data['description'])
                        # convert model to dict
                        return_data = model_to_dict(return_data)
                        return_data['category_name'] = category.name,
        except Exception as e:
            # unknown exception
            print(e)
            return_data = ERR_INTERNAL_ERROR

        # return json response
        return JsonResponse(return_data, safe=False)
    else:
        return JsonResponse(ERR_POST_EXPECTED)


# function to update the course contents
def update_course_contents(request, course_code):
    # only allows to update new_courseCode, new_category,
    # new_title, new_description if not published. To publish course, use
    # another url endpoint below
    # post data must contain new_courseCode, new_category, new_title, new_description
    if request.method == 'POST':
        try:
            # get request body and decode
            decoded_body = request.body.decode('utf-8')
            post_data = json.loads(decoded_body)

            # check for presence of all fields
            if not all_fields_present(post_data, ['new_courseCode', 'new_category', 'new_title', 'new_description']):
                return JsonResponse(ERR_REQUIRED_FIELD_ABS)

            new_course_code = post_data['new_courseCode']
            new_category = post_data['new_category']
            new_title = post_data['new_title']
            new_description = post_data['new_description']

            course = get_course(course_code)
            if not course:
                return JsonResponse(ERR_COURSE_DOES_NOT_EXIST)

            category = Category.objects.filter(name=new_category)
            if category.count() == 0:
                return JsonResponse(ERR_CATEGORY_DOES_NOT_EXIST)

            if course.isPublished:
                return JsonResponse(ERR_COURSE_ALREADY_PUBLISHED)

            course.courseCode = new_course_code
            course.category = category[0]
            course.title = new_title
            course.description = new_description
            course.save()
            return JsonResponse(model_to_dict(course))
        except Exception as e:
            print(e)
            return JsonResponse(ERR_INTERNAL_ERROR)

        # return json response
        return JsonResponse(return_data, safe=False)
    else:
        return JsonResponse(ERR_POST_EXPECTED)


# function to return the course description
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
            return_data['module_count'] = course.module_set.count()
            return_data['category_name'] = course.category.name

            sorted_module_set = __get_sorted_module_set(course)
            for module in sorted_module_set:  # for each module get the list of components
                module = module[1]  # the second item of the tuple
                module_dict = model_to_dict(module)
                all_components = __get_all_components(module)
                module_dict['component_count'] = len(all_components)
                module_dict['components'] = all_components
                module_data.append(module_dict)  # append module info to module data list
            return_data['modules'] = module_data  # list of all modules for the course
    except Exception as e:
        print(e)
        return_data = ERR_INTERNAL_ERROR
    return JsonResponse(return_data)


# function to publish a course
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
                    return_data['category_name'] = course.category.name
        except Exception as e:
            print(e)
            return_data = ERR_INTERNAL_ERROR
    else:
        return_data = ERR_POST_EXPECTED
    return JsonResponse(return_data)


# function to return all the courses in the database
def index(request):
    try:
        if request.method == 'GET':
            courses = []
            course_set = Course.objects.filter(isPublished=True);
            if course_set.count() > 0:
                for course in course_set:
                    data = model_to_dict(course)
                    data['category_name'] = course.category.name
                    courses.append(data)

            return JsonResponse({"all_courses": courses})
        else:
            return JsonResponse(ERR_GET_EXPECTED)
    except Exception as e:
        print(e)
        return JsonResponse(ERR_INTERNAL_ERROR)


# function to remove a course
def remove_course(request, course_code):
    if request.method == 'POST':
        course = get_course(course_code)
        if not course:
            return JsonResponse(ERR_COURSE_DOES_NOT_EXIST)

        if course.isPublished:
            return JsonResponse(ERR_COURSE_ALREADY_PUBLISHED)  # do not allow to delete a published course

        course.delete()
        return JsonResponse({'success': True, 'message': 'Course has been deleted'})

    else:
        return JsonResponse(ERR_POST_EXPECTED)


# -------------------------------------------------  MODULES  --------------------------------------------------------


# returns the sorted modules for the course specified
def __get_sorted_module_set(course):
    modules = []
    for module in course.module_set.all():
        modules.append((module.sequenceNumber, module))
    return sorted(modules)


# add a module to the database
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

            if course.isPublished:
                return JsonResponse(ERR_COURSE_ALREADY_PUBLISHED)

            module = course.module_set.create(moduleTitle=post_data['moduleTitle'],
                                              sequenceNumber=post_data['sequenceNumber'])
            return_data = model_to_dict(module)  # create module and set the return_data to new module created
    except Exception as e:
        print(e)
        return_data = ERR_INTERNAL_ERROR
    return JsonResponse(return_data)  # ask AK what to return


# update the module content in the database
def update_module_content(request, course_code, module_seq):
    module_seq = int(module_seq)
    # POST data must contain moduleTitle only, for changing the sequence number there's another url endpoint.
    if request.method == 'POST':
        post_data = json.loads(request.body.decode('utf-8'))

        if not all_fields_present(post_data, ['moduleTitle']):
            return JsonResponse(ERR_REQUIRED_FIELD_ABS)

        course = get_course(course_code)
        if not course:
            return JsonResponse(ERR_COURSE_DOES_NOT_EXIST)

        if course.isPublished:
            return JsonResponse(ERR_COURSE_ALREADY_PUBLISHED)

        module = course.module_set.filter(sequenceNumber=module_seq)
        if module.count() == 0:
            return JsonResponse(ERR_MOD_DOES_NOT_EXIST)
        module = module[0]
        module.moduleTitle = post_data['moduleTitle']
        module.save()
        return JsonResponse(model_to_dict(module))
    else:
        return JsonResponse(ERR_POST_EXPECTED)


# update the module order in the database
def update_module_order(request, course_code):
    # POST data must contain module_sequences attribute
    # module_sequences is an array of objects, each with id (module's id) and sequenceNumber
    # frontend check must be performed to ensure there are no modules with duplicate sequenceNumber
    # returns all updated modules in sorted order, ascending sequenceNumber

    post_data = json.loads(request.body.decode('utf-8'))
    updated = []
    if not all_fields_present(post_data, ['module_sequences']):
        return_data = ERR_REQUIRED_FIELD_ABS
    else:
        course = get_course(course_code)
        if not course:
            return_data = ERR_COURSE_DOES_NOT_EXIST
        else:
            if course.isPublished:
                return JsonResponse(ERR_COURSE_ALREADY_PUBLISHED)

            for obj in post_data['module_sequences']:
                module = course.module_set.filter(id=obj['id'])  # assumption: you will pass in the right module id
                if module.count() > 0:
                    module = module[0]
                    module.sequenceNumber = obj['sequenceNumber']
                    module.save()
                    updated.append((module.sequenceNumber, model_to_dict(module)))

            updated = sorted(updated, reverse=False)
            return_modules = []
            for mod in updated:
                return_modules.append(mod[1])
            return_data = {'updated_modules': return_modules}

    return JsonResponse(return_data)


# function to remove a module
def remove_module(request, course_code, module_seq):
    module_seq = int(module_seq)
    if request.method == 'POST':
        course = get_course(course_code)

        if not course:
            return JsonResponse(ERR_COURSE_DOES_NOT_EXIST)

        if course.isPublished:
            return JsonResponse(ERR_COURSE_ALREADY_PUBLISHED)  # do not allow to delete once published

        module = course.module_set.filter(sequenceNumber=module_seq)
        if module.count() == 0:
            return JsonResponse(ERR_MOD_DOES_NOT_EXIST)

        module = module[0]
        module.delete()
        return JsonResponse({'success': True, 'message': 'Module has been deleted'})
    else:
        return JsonResponse(ERR_POST_EXPECTED)


# ---------------------------------------------------COMPONENTS--------------------------------------------------------


# returns the component given the module, content type and component id
def __get_component(module, content_type, cmp_id):
    if module:
        if content_type == TEXT:
            cmp = module.textcomponent_set.filter(pk=cmp_id)
        elif content_type == IMG:
            cmp = module.imagecomponent_set.filter(pk=cmp_id)
        elif content_type == FILE:
            cmp = module.filecomponent_set.filter(pk=cmp_id)
        elif content_type == VIDEO:
            cmp = module.videocomponent_set.filter(pk=cmp_id)

        if cmp.count() == 0:
            return None
        return cmp[0]
    return None


# returns all the components for the module in sorted order
def __get_all_components(module):
    # returns all components of the specified module in sorted
    # order, ascending
    try:
        components = []
        # get all the components together
        for file_component in module.filecomponent_set.all():
            data = model_to_dict(file_component)
            data['contentType'] = FILE
            components.append((data['order'], data))
        for image_component in module.imagecomponent_set.all():
            data = model_to_dict(image_component)
            data['contentType'] = IMG
            components.append((data['order'], data))
        for text_component in module.textcomponent_set.all():
            data = model_to_dict(text_component)
            data['contentType'] = TEXT
            components.append((data['order'], data))
        for video_component in module.videocomponent_set.all():
            data = model_to_dict(video_component)
            data['contentType'] = VIDEO
            components.append((data['order'], data))

        # sort by order, ascending order
        components = sorted(components)
        return_components = []
        for cmp in components:
            return_components.append(cmp[1])  # get only the component. Discard order in tuple
        return return_components
    except Exception as e:
        print(e)
        return None


# helper function to create the appropriate component
def __create_new_component(post_data, module):
    # create the appropriate type of component according to the contentType specified
    if post_data:
        content_type = post_data['contentType']
        cmp = None
        if content_type == TEXT:
            cmp = module.textcomponent_set.create(order=post_data['order'],
                                                  content=post_data['content'],
                                                  contentTitle=post_data['contentTitle'])
        elif content_type == IMG:
            cmp = module.imagecomponent_set.create(order=post_data['order'],
                                                   content=post_data['content'],
                                                   contentTitle=post_data['contentTitle'])
        elif content_type == FILE:
            cmp = module.filecomponent_set.create(order=post_data['order'],
                                                  content=post_data['content'],
                                                  contentTitle=post_data['contentTitle'])
        elif content_type == VIDEO:
            cmp = module.videocomponent_set.create(order=post_data['order'],
                                                   content=post_data['content'],
                                                   contentTitle=post_data['contentTitle'])

        return cmp  # return new component
    else:
        return None


# helper function to check if component with the order specified exists
def __component_order_exists(module, order):
    # check if any of the components for the module have the order specified
    if module.filecomponent_set.filter(order=order).count() > 0 or module.imagecomponent_set.filter(
            order=order).count() > 0 or module.textcomponent_set.filter(
        order=order).count() > 0 or module.videocomponent_set.filter(order=order).count() > 0:
        return True
    return False


# helper function to update the component orders given the module and component sequence object
def __update_component_order(module, component_sequences):
    # confidence on the front end code right here !!!. orders passed in must be unique
    for seq in component_sequences:
        content_type = seq['contentType']
        cmp_id = seq['component_id']
        new_order = seq['order']

        component = __get_component(module, content_type, cmp_id)

        if component:
            component.order = new_order  # update order
            component.save()
    return __get_all_components(module)  # return all updated modules in order


# adds the component to the database
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
                if __component_order_exists(module, post_data['order']):
                    return JsonResponse(ERR_COMP_ORDER_EXISTS)

                component = __create_new_component(post_data, module)  # create the appropriate component

                if component:
                    return_data = model_to_dict(component)
                    return_data['contentType'] = component.contentType
                else:
                    return_data = {'failure': True, 'message': 'Component could not be created'}
    except Exception as e:
        print(e)
        return_data = ERR_INTERNAL_ERROR
    return JsonResponse(return_data)


# updates the component order in the database
def update_component_order(request, course_code, module_seq):
    module_seq = int(module_seq)
    # POST data must contain component_sequences attribute
    # component_sequences is an array of objects, each with id (component's id) and order and contentType
    # eg. {component_id: id, order: order, contentType: type}
    # Note: frontend check must be performed to ensure there are no component with duplicate order

    post_data = json.loads(request.body.decode('utf-8'))
    if not all_fields_present(post_data, ['component_sequences']):
        return_data = ERR_REQUIRED_FIELD_ABS
    else:
        course = get_course(course_code)
        if not course:
            return_data = ERR_COURSE_DOES_NOT_EXIST
        else:
            module = course.module_set.filter(sequenceNumber=module_seq)
            if module.count() == 0:
                return_data = ERR_MOD_DOES_NOT_EXIST
            else:
                module = module[0]  # get the first element
                updated_components = __update_component_order(module, post_data['component_sequences'])
                return_data = {'updated_components': updated_components}

    return JsonResponse(return_data)


# uploads only the file to the server
# to test
def upload_component(request, course_code, module_id):
    if request.method == 'POST':
        file = request.FILES['upload']
        relative_path = os.path.join(str(course_code), str(module_id), str(file))
        destination_path = os.path.join(settings.MEDIA_ROOT, relative_path)

        directory = os.path.dirname(destination_path)
        if not os.path.isdir(directory):
            os.makedirs(directory)

        destination = open(destination_path, 'wb+')
        for chunk in file.chunks():
            destination.write(chunk)
        destination.close()
        return JsonResponse({'success': True, 'file_path': relative_path,
                             'filename': str(file), 'base_folder': settings.MEDIA_URL})
    else:
        return JsonResponse(ERR_POST_EXPECTED)


# completely removes the component and its associated files if present
# to test
def remove_component(request, course_code, module_seq, component_id):
    # POST body must contain the contentType of the component
    if request.method == 'POST':
        post_data = json.loads(request.body.decode('utf-8'))
        if not all_fields_present(post_data, ['contentType']):
            return JsonResponse(ERR_REQUIRED_FIELD_ABS)

        content_type = post_data['contentType']

        course = Course.objects.filter(courseCode=course_code)
        if course.count() == 0:
            return JsonResponse(ERR_COURSE_DOES_NOT_EXIST)
        course = course[0]

        # if course.isPublished:
        #    return JsonResponse(ERR_COURSE_ALREADY_PUBLISHED)

        module = course.module_set.filter(sequenceNumber=module_seq)
        if module.count() == 0:
            return JsonResponse(ERR_MOD_DOES_NOT_EXIST)
        module = module[0]

        component = __get_component(module, content_type, component_id)

        if not component:
            return JsonResponse(ERR_COMP_DOES_NOT_EXIST)

        if content_type == TEXT:
            component.delete()
        else:
            path = os.path.join(settings.MEDIA_ROOT, component.content)
            if os.path.isfile(path):
                os.remove(path)
            component.delete()

        return JsonResponse({'success': True, 'message': 'Component removed'})
    else:
        return JsonResponse(ERR_POST_EXPECTED)


# ------------------------------------------ENROLL AND ENROLLMENT RECORDS -------------------------------------------


# function to enroll in a course
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
        elif Enrollment.objects.filter(participant_id=staff_id, isCompleted=False).count() > 0 \
                or Enrollment.objects.filter(participant_id=staff_id, isRetaking=True).count() > 0:
            # e = Enrollment.objects.filter(participant_id=staff_id, isRetaking=True)[0]
            # print('Course: ', e.course.title)
            # print('modules completed: ', e.modules_completed)
            # print(type(e.modules_completed))
            # print(type(e.course.module_set.count()))
            # print('module count: ', e.course.module_set.count())
            # already in one course
            return_data = ERR_ALREADY_ENROLLED_ONE
        elif Enrollment.objects.filter(course__courseCode=course.courseCode,
                                       participant_id=staff_id, isCompleted=True).count() > 0:
            # already completed this course
            return_data = ERR_ALREADY_COMPLETED_COURSE
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


# returns all the enrolled participants in a course
def get_enrolled_participants(request, course_code):
    try:
        course = get_course(course_code)
        if not course:
            return_data = ERR_COURSE_DOES_NOT_EXIST
        else:
            enrollments = Enrollment.objects.filter(course__courseCode=course_code)
            all_enrolls = []
            for enrollment in enrollments:
                if enrollment.isRetaking or not enrollment.isCompleted:
                    participant = Staff.objects.get(id=enrollment.participant.id)
                    enrollment = model_to_dict(enrollment)
                    enrollment['participant_info'] = {'username': participant.username}
                    all_enrolls.append(enrollment)
            return_data = {'all_enrolls': all_enrolls}
    except Exception as e:
        print(e)
        return_data = ERR_INTERNAL_ERROR
    return JsonResponse(return_data)


# returns all the participants who completed a course
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


# records the progress of a participant for the course
def update_course_progress(request):
    # POST body must contain course_id, staff_id, new_status (the number of modules completed from start)
    try:
        if request.method == 'POST':
            post_data = json.loads(request.body.decode('utf-8'))

            if not all_fields_present(post_data, ['course_id', 'staff_id', 'new_status']):
                return JsonResponse(ERR_REQUIRED_FIELD_ABS)

            course = Course.objects.filter(pk=post_data['course_id'])
            if course.count() == 0:
                return JsonResponse(ERR_COURSE_DOES_NOT_EXIST)

            staff = Staff.objects.filter(pk=post_data['staff_id'])
            if staff.count() == 0:
                return JsonResponse(ERR_STAFF_DOES_NOT_EXIST)

            enrollment = Enrollment.objects.filter(course=course, participant=staff)
            if enrollment.count() == 0:
                return JsonResponse(ERR_ENROLLMENT_RECORD_DOES_NOT_EXIST)

            course = course[0]
            enrollment = enrollment[0]
            new_status = post_data['new_status']
            if new_status == course.module_set.count():
                enrollment.isCompleted = True
                enrollment.isRetaking = False
                date = datetime.datetime.now()
                enrollment.date_completed = date.strftime('%Y-%m-%d')
                enrollment.save()
            if new_status <= course.module_set.count():
                enrollment.modules_completed = new_status
                enrollment.save()

            return JsonResponse(model_to_dict(enrollment))
        else:
            return JsonResponse(ERR_POST_EXPECTED)
    except Exception as e:
        print(e)
        return JsonResponse(ERR_INTERNAL_ERROR)


# function to drop a course
def drop_course(request):
    # POST body must contain course_id, staff_id, new_status (the number of modules completed from start)
    try:
        if request.method == 'POST':
            post_data = json.loads(request.body.decode('utf-8'))

            if not all_fields_present(post_data, ['course_id', 'staff_id', 'new_status']):
                return JsonResponse(ERR_REQUIRED_FIELD_ABS)

            course = Course.objects.filter(pk=post_data['course_id'])
            if course.count() == 0:
                return JsonResponse(ERR_COURSE_DOES_NOT_EXIST)

            staff = Staff.objects.filter(pk=post_data['staff_id'])
            if staff.count() == 0:
                return JsonResponse(ERR_STAFF_DOES_NOT_EXIST)

            enrollment = Enrollment.objects.filter(course=course, participant=staff)
            if enrollment.count() == 0:
                return JsonResponse(ERR_ENROLLMENT_RECORD_DOES_NOT_EXIST)

            # delete enrollment record
            enrollment = enrollment[0]
            if enrollment.isCompleted:
                enrollment.modules_completed = enrollment.course.module_set.count()
                enrollment.isRetaking = False
                enrollment.save()
            else:
                enrollment.delete()
            return JsonResponse({'success': True, 'message': 'Current course successfully dropped'})
        else:
            return JsonResponse(ERR_POST_EXPECTED)
    except Exception as e:
        print(e)
        return JsonResponse(ERR_INTERNAL_ERROR)


# function to retake a course
def retake_course(request):
    # POST body must contain course_id, staff_id
    try:
        if request.method == 'POST':
            post_data = json.loads(request.body.decode('utf-8'))

            if not all_fields_present(post_data, ['course_id', 'staff_id']):
                return JsonResponse(ERR_REQUIRED_FIELD_ABS)

            course = Course.objects.filter(pk=post_data['course_id'])
            if course.count() == 0:
                return JsonResponse(ERR_COURSE_DOES_NOT_EXIST)

            staff = Staff.objects.filter(pk=post_data['staff_id'])
            if staff.count() == 0:
                return JsonResponse(ERR_STAFF_DOES_NOT_EXIST)

            enrollment = Enrollment.objects.filter(course=course, participant=staff)
            if enrollment.count() == 0:
                return JsonResponse(ERR_ENROLLMENT_RECORD_DOES_NOT_EXIST)

            enrollment = enrollment[0]
            if not enrollment.isCompleted:
                return JsonResponse(ERR_CANNOT_RETAKE)

            if Enrollment.objects.filter(participant=staff, isCompleted=False).count() > 0 \
                    or Enrollment.objects.filter(participant=staff, isRetaking=True).count() > 0:
                # already in one course
                return JsonResponse(ERR_ALREADY_ENROLLED_ONE)

            enrollment.modules_completed = 0
            enrollment.isRetaking = True  # set the isRetaking flag
            enrollment.save()
            return JsonResponse(model_to_dict(enrollment))
        else:
            return JsonResponse(ERR_POST_EXPECTED)
    except Exception as e:
        print(e)
        return JsonResponse(ERR_INTERNAL_ERROR)


# --------------------------------------------------EXPERIMENTAL (REMOVE) ---------------------------------------

def uploadTest(request):
    return render(request, 'courses/uploadtest.html')


from django.conf import settings


def uploadfiletest(request):
    if request.method == 'POST':
        print(request.POST['extra_info'])
        file = request.FILES['upload']
        destination = open(os.path.join(settings.MEDIA_ROOT, str(file)), 'wb+')
        for chunk in file.chunks():
            destination.write(chunk)
        destination.close()
        return JsonResponse({'success': True, 'file_path': os.path.join(settings.MEDIA_URL, str(file)),
                             'filename': str(file)})


def removefiletest(request):
    # post_data = json.loads(request.body.decode('utf-8'))
    path = os.path.join(settings.MEDIA_ROOT, 'trolltunga.jpg')
    os.remove(path)
    return JsonResponse({'success': True})


def add_course(request):
    from .forms.CreateCourse import CreateCourse
    from django.http import HttpResponseRedirect

    if request.method == 'POST':
        form = CreateCourse(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/thanks')
    else:
        form = CreateCourse()
    return render(request, 'courses/addCourse.html', {'form': form})


def thanks(response):
    from django.http import HttpResponse
    return HttpResponse('<h1> Thanks</h1>')
