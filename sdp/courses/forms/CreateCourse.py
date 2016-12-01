from courses.models import Course
from django.forms import ModelForm

class CreateCourse(ModelForm):
    class Meta:
        model = Course
        fields = ['instructor', 'category', 'courseCode', 'description']