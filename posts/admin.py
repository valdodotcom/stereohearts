from django.contrib import admin

# Register your models here.
from .models import Review, MusicList

admin.site.register(Review)
admin.site.register(MusicList)