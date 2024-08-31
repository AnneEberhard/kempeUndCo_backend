from django.urls import path
from .views import CreateDiscussionEntryView, DiscussionEntryDetailView, DiscussionListView, get_or_create_discussion

urlpatterns = [
    path('entries/', CreateDiscussionEntryView.as_view(), name='create_discussion_entry'),
    path('entries/<int:pk>/', DiscussionEntryDetailView.as_view(), name='discussion_entry_detail'),
    path('<str:id>/', get_or_create_discussion, name='get_or_create_discussion'),
    path('', DiscussionListView.as_view(), name='get_all_discussions'),
]
