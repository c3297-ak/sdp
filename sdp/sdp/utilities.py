# Custom error messages
ERR_COURSE_DOES_NOT_EXIST = {'failure': True, 'message': 'Course does not exist'}
ERR_MOD_DOES_NOT_EXIST = {'failure': True, 'message': 'Module does not exist'}
ERR_COMP_DOES_NOT_EXIST = {'failure': True, 'message': 'Component does not exist'}
ERR_NO_INSTRUCTOR_PERMISSION = {'failure': True, 'message': 'Instructor permission not assigned'}
ERR_PARTICIPANT_DOES_NOT_EXIST = {'failure': True, 'message': 'Participant does not exist'}
ERR_STAFF_DOES_NOT_EXIST = {'failure': True, 'message': 'Staff does not exist'}
ERR_STAFF_INCORRECT_PASSWORD = {'failure': True, 'message': 'Incorrect password'}
ERR_STAFF_ALREADY_EXIST = {'failure': True, 'message': 'Staff already exist'}
ERR_INTERNAL_ERROR = {'failure': True, 'message': 'Internal server error'}
ERR_REQUIRED_FIELD_ABS = {'failure': True, 'message': 'All required fields are not present in POST data'}
ERR_COMP_ORDER_EXISTS = {"failure": True, 'message': 'Component with the same order already exists'}
ERR_MOD_ORDER_EXISTS = {"failure": True, 'message': 'Module with the same order already exists'}
ERR_POST_EXPECTED = {'failure': True, 'message': 'Use POST request'}
ERR_GET_EXPECTED = {'failure': True, 'message': 'Use GET request'}
ERR_ALREADY_ENROLLED_ONE = {'failure': True, 'message': 'Already enrolled in one course'}
ERR_ALREADY_ENROLLED_CURR = {'failure': True, 'message': 'Already enrolled in this course'}
ERR_ALREADY_COMPLETED_COURSE = {'failure': True, 'message': 'Already completed the course'}
ERR_ENROLLMENT_RECORD_DOES_NOT_EXIST = {'failure': True, 'message': 'No enrollment record'}
ERR_PARTICIPANT_INSTRUCT_SAME = {'failure': True, 'message': 'You cannot enroll in a course you created'}
ERR_COURSE_NOT_PUBLISHED = {'failure': True, 'message': 'You cannot enroll in a course that is not published'}
ERR_COURSE_ALREADY_PUBLISHED = {'failure': True, 'message': 'Course already published. Not allowed to make major changes'}
ERR_CATEGORY_ALREADY_EXISTS = {'failure': True, 'message': 'Category already exists'}
ERR_CATEGORY_DOES_NOT_EXIST = {'failure': True, 'message': 'Category does not exist'}
ERR_CANNOT_RETAKE = {'failure': True, 'message': 'Cannot retake course. Complete it first to retake!'}
ERR_PERMISSION_EXIST = {'failure': True, 'message': 'Already granted permission'}

# File types
TEXT = 'text'
VIDEO = 'video'
IMG = 'image'
FILE = 'file'


def all_fields_present(data, field_lst):
    for field in field_lst:
        if field not in data:
            return False
    return True
