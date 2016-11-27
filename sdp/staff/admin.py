from django.contrib import admin

# Register your models here.
from .models import Staff, Instructor, Participant, Administrator, HumanResource

admin.site.register(Staff)
admin.site.register(Instructor)
admin.site.register(Participant)
admin.site.register(Administrator)
admin.site.register(HumanResource)