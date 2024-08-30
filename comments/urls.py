from django.urls import path
from .views import CommentCreateView, CommentDetailView, CommentListView

urlpatterns = [
    path('create/', CommentCreateView.as_view(), name='comment-create'),
    path('<int:pk>/', CommentDetailView.as_view(), name='comment-detail'),
    path('', CommentListView.as_view(), name='comment-list'),
]
