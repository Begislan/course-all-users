from django.contrib import admin
from front.models import Course, Lesson, Content

# Register your models here.
admin.site.register(Content)
admin.site.register(Course)
admin.site.register(Lesson)