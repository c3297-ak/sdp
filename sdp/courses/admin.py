from django.contrib import admin

# Register your models here.
from .models import FileComponent, TextComponent, ImageComponent,Course, Module, Enrollment

admin.site.register(FileComponent)
admin.site.register(TextComponent)
admin.site.register(ImageComponent)
admin.site.register(Module)
admin.site.register(Enrollment)
admin.site.register(Course)
