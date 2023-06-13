from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Review)
admin.site.register(ReviewComment)
admin.site.register(ReviewFavourite)
admin.site.register(ReviewUpvote)
admin.site.register(ReviewDownvote)

admin.site.register(MusicList)
admin.site.register(ListComment)
admin.site.register(ListFavourite)
admin.site.register(ListUpvote)
admin.site.register(ListDownvote)