from django.conf.urls import url, include
from . import views

app_name = 'courses'

urlpatterns = [
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
    url(r'^(?P<course_code>[a-zA-Z0-9]+)/publish', views.publishCourse, name='publish'),
    url(r'^(?P<course_code>[a-zA-Z0-9]+)/enrolled', views.get_enrolled_participants, name='get_enrolled'),
    url(r'^(?P<course_code>[a-zA-Z0-9]+)/completed', views.get_completed_participants, name='get_completed'),
    url(r'^(?P<course_code>[a-zA-Z0-9]+)/updatedModuleOrder$', views.update_module_order, name='updatedModuleOrder$'),
    url(r'^(?P<course_code>[a-zA-Z0-9]+)/modules/(?P<module_seq>[0-9]+)/updatedComponentOrder$',
        views.update_module_order, name='updatedComponentOrder$'),
    url(r'^(?P<course_code>[a-zA-Z0-9]+)/modules/(?P<module_seq>[0-9]+)/upload$',
        views.upload_component, name='upload_component'),
    url(r'^/remove$', views.remove_component, name='remove_component'),

]
