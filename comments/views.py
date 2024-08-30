from rest_framework import generics, status
from .models import Comment
from .serializers import CommentSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404



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


class CommentDetailView(APIView):
    def get(self, request, pk, *args, **kwargs):
        """
        Gibt die Details eines Kommentars zurück.
        """
        comment = get_object_or_404(Comment, pk=pk)
        serializer = CommentSerializer(comment, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk, *args, **kwargs):
        """
        Bearbeitet einen Kommentar.
        """
        comment = get_object_or_404(Comment, pk=pk)
        serializer = CommentSerializer(comment, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        """
        Löscht einen Kommentar.
        """
        comment = get_object_or_404(Comment, pk=pk)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)