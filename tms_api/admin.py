from django.contrib import admin

from tms_api.models import CUser, Project, Task

# Register your models here.
admin.site.register(CUser)
admin.site.register(Project)
admin.site.register(Task)
