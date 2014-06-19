from django.contrib import admin
from firstapp.models import Student,Course,StudentState,CourseDependency, Question

# Register your models here.

admin.site.register(Student)
admin.site.register(Course)
admin.site.register(StudentState)
admin.site.register(CourseDependency)
admin.site.register(Question)
