from django.conf.urls import url, include
from . import views

app_name = 'courses'

urlpatterns = [
    # ----------------------------------- CATEGORIES ---------------------------------------------------------------

    # add a new category
    url(r'^addCategory', views.add_category, name='addCategory'),

    # get all categories
    url(r'^categories', views.get_categories, name='allCategories'),

    # remove a category. Check function for POST body requirements
    url(r'^category/remove', views.remove_category, name='removeCategory'),

    # ----------------------------------  COURSES ------------------------------------------------------------------

    # get all published courses
    url(r'^$', views.index, name='index'),


    # courses/addCourse. Add a course to the database
    url(r'^addCourse$', views.addCourse, name='addCourse'),


    # courses/<course_code>. Get the description for a particular course
    url(r'^(?P<course_code>[a-zA-Z0-9]+)/$', views.courseDescription, name='courseDescription'),


    # courses/<course_code>/update_course_contents. Update the contents of a course
    url(r'^(?P<course_code>[a-zA-Z0-9]+)/update_course_contents$', views.update_course_contents, name='update_course'),


    # courses/<course_code>/publish
    # POST request to publish a course. Check function for required POST body
    url(r'^(?P<course_code>[a-zA-Z0-9]+)/publish', views.publishCourse, name='publish'),


    # courses/<course_code>/remove
    # removes a course from the database if not published. POST body empty.
    url(r'^(?P<course_code>[a-zA-Z0-9]+)/remove$', views.remove_course, name='remove_course'),


    # --------------------------------------------- MODULES -----------------------------------------------------------


    # courses/<course_code>/addModule.  Add a module to the course
    url(r'^(?P<course_code>[a-zA-Z0-9]+)/addModule$', views.addModule, name='addModule'),


    # courses/<course_code>/modules/<module_seq>/update_content. Update module content (moduleTitle). Check function
    # for POST body requirements
    url(r'^(?P<course_code>[a-zA-Z0-9]+)/modules/(?P<module_seq>[a-zA-Z0-9]+)/update_content$',
        views.update_module_content, name='update_module_content'),


    # courses/<course_code>/update_module_order. Update module order. Check function
    # POST request to update the module order for a course. Check function for required POST body
    url(r'^(?P<course_code>[a-zA-Z0-9]+)/update_module_order', views.update_module_order, name='update_module_order'),


    # courses/<course_code>/modules/<module_seq>/remove. Remove a module if course not published
    url(r'^(?P<course_code>[a-zA-Z0-9]+)/modules/(?P<module_seq>[a-zA-Z0-9]+)/remove', views.remove_module,
        name='remove_module'),


    # ------------------------------------------- COMPONENTS ----------------------------------------------------


    # courses/<course_code>/modules/<module_seq>/addComponent
    url(r'^(?P<course_code>[a-zA-Z0-9]+)/modules/(?P<module_seq>[0-9]+)/addComponent$', views.addComponent,
        name='addComponent'),


    # courses/<course_code>/modules/<module_seq>/update_component_order
    # POST request to update component order of a module in a course. Check function for required POST body
    url(r'^(?P<course_code>[a-zA-Z0-9]+)/modules/(?P<module_seq>[0-9]+)/update_component_order',
        views.update_component_order, name='update_component_order'),


    # courses/<course_code>/modules/<module_seq>/upload_component
    # POST request to upload a component. Check function for required POST body
    url(r'^(?P<course_code>[a-zA-Z0-9]+)/modules/(?P<module_id>[0-9]+)/upload_component$',
        views.upload_component, name='upload_component'),


    # courses/<course_code>/modules/<module_seq>/components/<component_id>/remove
    # POST request to remove a component of a module. Check function for required POST body
    url(r'^(?P<course_code>[a-zA-Z0-9]+)/modules/(?P<module_seq>[0-9]+)/components/(?P<component_id>[0-9]+)/remove$',
        views.remove_component, name='remove_component'),


    # NOTE : NO specific url to update component content. Remove the previous component with the id and then add a
    # new one with the updates specified. Removal will be disallowed if course is already published


    # ------------------------------------------- ENROLL AND ENROLLMENT ----------------------------------------------


    # courses/<course_code>/enroll. Enroll in a course
    url(r'^(?P<course_code>[a-zA-Z0-9]+)/enroll$', views.enroll, name='enroll'),


    # courses/<course_code>/enrolled
    # GET request to get all the participants enrolled in a course
    url(r'^(?P<course_code>[a-zA-Z0-9]+)/enrolled', views.get_enrolled_participants, name='get_enrolled'),


    # courses/<course_code>/completed
    # GET request to get all the participants who completed a course
    url(r'^(?P<course_code>[a-zA-Z0-9]+)/completed', views.get_completed_participants, name='get_completed'),


    # PERSONAL OPINION: THE FOLLOWING SHOULD NOT BE A PART OF THE COURSE APP AND SHOULD BE MOVED TO THE STAFF APP IF
    # POSSIBLE. AK'S IN CHARGE OF THAT


    # courses/update_course_progress
    # POST request to update the course progress for a staff. Check function for required POST body
    url(r'^update_course_progress', views.update_course_progress, name='update_course_progress'),


    # courses/drop_course
    # POST request to drop a course by a staff
    url(r'^drop_course', views.drop_course, name='drop_course'),


    # courses/retake_course
    # POST request to drop a course by a staff
    url(r'^retake_course$', views.retake_course, name='retake_course'),


    # ------------------------------------------------- EXPERIMENTAL --------------------------------------------------



    url(r'^uploadfiletest', views.uploadfiletest),
    url(r'^deletefiletest', views.removefiletest),
    url(r'^uploadtest', views.uploadTest),
    url(r'add_course_exp$', views.add_course),
    url(r'thanks/', views.thanks),

]
