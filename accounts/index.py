from algoliasearch_django import AlgoliaIndex
from algoliasearch_django.decorators import register

from .models import User

@register(User)
class UserIndex(AlgoliaIndex):
    fields = [
        'username', 
        'display_name',
    ]
