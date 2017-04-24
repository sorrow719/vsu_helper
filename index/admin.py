from django.contrib import admin

from django.contrib import admin
from django.contrib.sites.models import Site

from index.models import *

# Register your models here.
admin.site.register(AcademicSubject)
admin.site.register(Department)
admin.site.register(Direction)