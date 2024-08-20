from django.urls import path
from .views import CreateDiscussionEntryView, get_all_discussions, get_or_create_discussion


urlpatterns = [
    path('entries/', CreateDiscussionEntryView.as_view(), name='create_discussion_entry'),
    path('<str:id>/', get_or_create_discussion, name='get_or_create_discussion'),
    path('', get_all_discussions, name='get_all_discussions'),
    
]
