from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Review)
admin.site.register(ReviewVote)
admin.site.register(ReviewComment)
admin.site.register(ReviewCommentVote)

admin.site.register(MusicList)
admin.site.register(ListVote)
admin.site.register(ListComment)
admin.site.register(ListCommentVote)