from rest_framework import generics, status
from .models import Comment
from .serializers import CommentSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404


class CommentCreateView(generics.CreateAPIView):
    """
    API view to create a new comment.

    * Requires authentication.
    * Automatically sets the `author` field to the currently authenticated user.
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        """
        Save the comment with the `author` field set to the current user.

        Args:
            serializer (CommentSerializer): The serializer instance used to validate and save the comment.
        """
        serializer.save(author=self.request.user)


class CommentListView(generics.ListAPIView):
    """
    API view to list all comments or filter comments based on query parameters.

    * Supports optional filtering by 'info' or 'recipe' ID.
    * Requires authentication.
    """
    serializer_class = CommentSerializer

    def get_queryset(self):
        """
        Get the list of comments, optionally filtered by 'info' or 'recipe' ID.

        Returns:
            QuerySet: A QuerySet of comments that match the filtering criteria, if any.
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
    """
    API view to retrieve, update, or delete a specific comment.

    * Requires authentication for update and delete operations.
    """

    def get(self, request, pk, *args, **kwargs):
        """
        Retrieve a specific comment by its primary key (PK).

        Args:
            request (Request): The HTTP request object.
            pk (int): The primary key of the comment to retrieve.

        Returns:
            Response: A response containing the comment's details if found, or a 404 error if not.
        """
        comment = get_object_or_404(Comment, pk=pk)
        serializer = CommentSerializer(comment, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk, *args, **kwargs):
        """
        Update a specific comment by its primary key (PK).

        Args:
            request (Request): The HTTP request object with the updated comment data.
            pk (int): The primary key of the comment to update.

        Returns:
            Response: A response containing the updated comment data if successful, or validation errors if not.
        """
        comment = get_object_or_404(Comment, pk=pk)
        serializer = CommentSerializer(comment, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        """
        Delete a specific comment by its primary key (PK).

        Args:
            request (Request): The HTTP request object.
            pk (int): The primary key of the comment to delete.

        Returns:
            Response: A response with a 204 status if the comment was deleted successfully, or a 404 error if not found.
        """
        comment = get_object_or_404(Comment, pk=pk)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
