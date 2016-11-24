from django.contrib import admin

# Register your models here.
from .models import Staff, Instructor, Participant

admin.site.register(Staff)
admin.site.register(Instructor)
admin.site.register(Participant)