from algoliasearch_django import AlgoliaIndex
from algoliasearch_django.decorators import register

from .models import Review, MusicList

@register(Review)
class ReviewIndex(AlgoliaIndex):
    fields = [
        'title', 
        'project',
        'user'
    ]

@register(MusicList)
class MusicListIndex(AlgoliaIndex):
    fields = [
        'title', 
        'user',
        'get_projects_list'
    ]
