from rest_framework import generics
from .models import Comment
from .serializers import CommentSerializer


class CommentCreateView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentListView(generics.ListAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        """
        Optionale Filterung nach 'info' oder 'recipe' ID.
        """
        queryset = Comment.objects.all()
        info_id = self.request.query_params.get('info')
        recipe_id = self.request.query_params.get('recipe')
        if info_id:
            queryset = queryset.filter(info_id=info_id)
        elif recipe_id:
            queryset = queryset.filter(recipe_id=recipe_id)
        return queryset
