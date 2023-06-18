from rest_framework.decorators import api_view
from rest_framework.response import Response
from projects.models import Project, Artist
from .serializers import *
from .permissions import IsModeratorOrReadOnly
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.exceptions import PermissionDenied

@api_view(['GET'])
def getRoutes(request):
    routes = [
        'GET /projects/',
        'GET /projects/view-projects/',
        'GET /projects/view-projects/project_id',
        'GET /projects/view-artists/',
        'GET /projects/view-artists/artist_id', 
    ]

    return Response(routes) 


class ProjectView(ListCreateAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [IsModeratorOrReadOnly]

    def get_queryset(self):
        artist = self.request.query_params.get('artist', None)
        queryset = Project.objects.all().order_by('-created_at')

        if artist:
            queryset = queryset.filter(artist__name=artist)
        return queryset

    def perform_create(self, serializer):
        if not self.request.user.is_moderator:
            raise PermissionDenied("You are not authorized to create a new project.")
        return super().perform_create(serializer)
    

class ProjectDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsModeratorOrReadOnly]


class ArtistView(ListCreateAPIView):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
    permission_classes = [IsModeratorOrReadOnly]

    def perform_create(self, serializer):
        if not self.request.user.is_moderator:
            raise PermissionDenied("You are not authorized to create a new artist.")
        return super().perform_create(serializer)

class ArtistDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
    permission_classes = [IsModeratorOrReadOnly]
