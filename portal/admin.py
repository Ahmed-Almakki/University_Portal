from django.contrib import admin

# Register your models here.
from .models import Group, Classroom, Discipline, Lesson, Grade, Application, Announcement, Document

admin.site.register(Group)
admin.site.register(Classroom)
admin.site.register(Discipline)
admin.site.register(Lesson)
admin.site.register(Grade)
admin.site.register(Application)
admin.site.register(Announcement)
admin.site.register(Document)