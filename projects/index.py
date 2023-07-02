from algoliasearch_django import AlgoliaIndex
from algoliasearch_django.decorators import register

from .models import Project, Artist

@register(Project)
class ProjectIndex(AlgoliaIndex):
    fields = [
        'title', 
        'artist',
        'release_date'
    ]

@register(Artist)
class ArtistIndex(AlgoliaIndex):
    fields = [
        'name',
        'get_projects_list'
    ]
