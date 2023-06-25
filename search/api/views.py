from rest_framework import generics
from rest_framework.response import Response
from .. import client

class SearchListView(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        query = request.GET.get('q')
        tag = request.GET.get('tag')
        if not query:
            return Response('', status=400)
        results = client.perform_search(query)
        return Response(results)