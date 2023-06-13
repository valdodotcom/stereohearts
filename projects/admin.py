from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Artist)
admin.site.register(Project)