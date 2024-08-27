from django.urls import path
from .views import CommentCreateView, CommentListView

urlpatterns = [
    path('create/', CommentCreateView.as_view(), name='comment-create'),
    path('', CommentListView.as_view(), name='comment-list'),
]
