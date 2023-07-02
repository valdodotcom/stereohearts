from rest_framework import generics
from rest_framework.response import Response
from .. import client

class SearchListView(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        query = request.GET.get('q')
        tag = request.GET.get('tag')
        if not query:
            return Response('', status=400)
        results = client.perform_search(query, 'search_MusicList')
        return Response(results)
    
class SearchReviewView(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        query = request.GET.get('q')
        tag = request.GET.get('tag')
        if not query:
            return Response('', status=400)
        results = client.perform_search(query, 'search_Review')
        return Response(results)

class SearchUserView(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        query = request.GET.get('q')
        tag = request.GET.get('tag')
        if not query:
            return Response('', status=400)
        results = client.perform_search(query, 'search_User')
        return Response(results)    

class SearchProjectView(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        query = request.GET.get('q')
        tag = request.GET.get('tag')
        if not query:
            return Response('', status=400)
        results = client.perform_search(query, 'search_Project')
        return Response(results)
    
class SearchArtistView(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        query = request.GET.get('q')
        tag = request.GET.get('tag')
        if not query:
            return Response('', status=400)
        results = client.perform_search(query, 'search_Artist')
        return Response(results)

class SearchAllView(generics.GenericAPIView):
    def get_queryset(self):
        pass
    
    def get(self, request, *args, **kwargs):
        query = request.GET.get('q')
        tag = request.GET.get('tag')
        if not query:
            return Response('', status=400)     
        results = client.get_multiple_queries(query)
        print(results)
        return Response(results)