from django.contrib import admin
from .models import Assignment, Submission, Course

admin.site.register(Assignment)
admin.site.register(Submission)
admin.site.register(Course)