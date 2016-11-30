from django.conf.urls import url, include
from . import views

app_name = 'courses'

urlpatterns = [
    # add a new category
    url(r'^addCategory', views.add_category, name='addCategory'),

    # get all categories
    url(r'^categories', views.get_categories, name='allCategories'),

    # remove a category
    url(r'^category/remove', views.remove_category, name='removeCategory'),

    # courses/
    url(r'^$', views.index, name='index'),

    # courses/addCourse
    url(r'^addCourse$', views.addCourse, name='addCourse'),

    # courses/71/addModule
    url(r'^(?P<course_code>[a-zA-Z0-9]+)/addModule$', views.addModule, name='addModule'),

    # courses/71/modules/12/addComponent
    url(r'^(?P<course_code>[a-zA-Z0-9]+)/modules/(?P<module_seq>[0-9]+)/addComponent$', views.addComponent,
        name='addComponent'),

    # courses/71
    url(r'^(?P<course_code>[a-zA-Z0-9]+)/$', views.courseDescription, name='courseDescription'),

    # courses/71/enroll
    url(r'^(?P<course_code>[a-zA-Z0-9]+)/enroll$', views.enroll, name='enroll'),

    # POST request to publish a course. Check function for required POST body
    url(r'^(?P<course_code>[a-zA-Z0-9]+)/publish', views.publishCourse, name='publish'),

    # GET request to get all the participants enrolled in a course
    url(r'^(?P<course_code>[a-zA-Z0-9]+)/enrolled', views.get_enrolled_participants, name='get_enrolled'),

    # GET request to get all the participants who completed a course
    url(r'^(?P<course_code>[a-zA-Z0-9]+)/completed', views.get_completed_participants, name='get_completed'),

    # POST request to update the module order for a course. Check function for required POST body
    url(r'^(?P<course_code>[a-zA-Z0-9]+)/updatedModuleOrder$', views.update_module_order, name='updatedModuleOrder$'),

    # POST request to update component order of a module in a course. Check function for required POST body
    url(r'^(?P<course_code>[a-zA-Z0-9]+)/modules/(?P<module_seq>[0-9]+)/updatedComponentOrder$',
        views.update_module_order, name='updatedComponentOrder$'),

    # POST request to upload a component. Check function for required POST body
    url(r'^(?P<course_code>[a-zA-Z0-9]+)/modules/(?P<module_seq>[0-9]+)/uploa d$',
        views.upload_component, name='upload_component'),

    # POST request to remove a component of a module. Check function for required POST body
    url(r'^module/remove$', views.remove_component, name='remove_component'),

    # POST request to update the course progress for a staff. Check function for required POST body
    url(r'^update_course_progress', views.update_course_progress, name='update_course_progress'),

]
