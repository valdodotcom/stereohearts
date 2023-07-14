from rest_framework.decorators import api_view
from rest_framework.response import Response
from posts.models import Review, MusicList
from .serializers import *
from .permissions import IsPostOwnerOrReadOnly
from .mixins import PostViewMixin, PostVoteMixin, PostCommentMixin
from rest_framework.generics import CreateAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

@api_view(['GET'])
def getRoutes(request):
    routes = [
        'GET /posts/',
        'GET /posts/reviews/',
        'GET /posts/reviews/?username=:username',
        'GET /posts/reviews/review_id',
        'GET /posts/lists/', 
        'GET /posts/lists/?username=:username',
        'GET /posts/lists/list_id',
    ]

    return Response(routes) 


class ReviewView(PostViewMixin, ListCreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    model = Review

class ReviewDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsPostOwnerOrReadOnly]
    queryset = Review.objects.all()

class ReviewVoteView(PostVoteMixin ,CreateAPIView):
    serializer_class = ReviewVoteSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    model = ReviewVote

    def perform_create(self, serializer):
        super().perform_create(serializer, 'review_id')

class ReviewCommentView(PostCommentMixin, CreateAPIView):
    serializer_class = ReviewCommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    model = ReviewComment
    
    def perform_create(self, serializer):
        super().perform_create(serializer, 'review', Review)

class ReviewCommentVoteView(PostVoteMixin, CreateAPIView):
    serializer_class = ReviewCommentVoteSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    model = ReviewCommentVote

    def perform_create(self, serializer):
        super().perform_create(serializer, 'review_comment_id')

class ListView(PostViewMixin, ListCreateAPIView):
    serializer_class = ListSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    model = MusicList

class ListDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = ListSerializer
    permission_classes = [IsPostOwnerOrReadOnly]
    queryset = MusicList.objects.all()

class ListVoteView(PostVoteMixin, CreateAPIView):
    serializer_class = ListVoteSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    model = ListVote

    def perform_create(self, serializer):
        super().perform_create(serializer, 'music_list_id')

class ListCommentView(PostCommentMixin, CreateAPIView):
    serializer_class = ListCommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    model = ListComment
    
    def perform_create(self, serializer):
        super().perform_create(serializer, 'music_list', MusicList)

class ListCommentVoteView(PostVoteMixin, CreateAPIView):
    serializer_class = ListCommentVoteSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    model = ListCommentVote

    def perform_create(self, serializer):
        super().perform_create(serializer, 'list_comment_id')


class CreateReview(CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    queryset = Review.objects.all()

    def perform_create(self, serializer):
        user = self.request.user
        project = self.request.data.get('project')  # Get project from request data
        serializer.save(user=user, project=project)
        return super().perform_create(serializer)
    

class MusicListViewSet(ModelViewSet):
    serializer_class = ListSerializer
    permission_classes = [IsAuthenticated]
    queryset = MusicList.objects.all()

    def user_has_list(self, list_id):
        user_lists = MusicList.objects.filter(user=self.request.user)
        return user_lists.filter(id=list_id).exists()

    def create(self, request, *args, **kwargs):
        list_id = request.data.get('list_id')
        project = request.data.get('project')
        title = request.data.get('title')
        body = request.data.get('body')
        new_list = None

        if self.user_has_list(list_id):
            existing_list = MusicList.objects.get(id=list_id)
            existing_list.user = self.request.user
            projects_list = existing_list.projects.split(',')

            if project is not None:  # Check if 'project' field is not null
                existing_list.projects = project

            if title is not None:  # Check if 'title' field is not null
                existing_list.title = title

            if body is not None:  # Check if 'body' field is not null
                existing_list.body = body

            if project not in projects_list:  # Check if the project ID is already in the list
                projects_list.append(project)
                existing_list.projects = ','.join(projects_list)
                existing_list.save()
            else:
                return Response({"error": "item already in list"})
        else:
            new_list = MusicList.objects.create(user=self.request.user, 
                                                projects=project, title=title, body=body,
                                                )

            serializer = self.get_serializer(new_list)
            return Response(serializer.data, status=201)
        serializer = self.get_serializer(existing_list)
        return Response(serializer.data, status=201)