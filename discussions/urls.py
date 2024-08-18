from django.urls import path
from .views import get_all_discussions, get_or_create_discussion


urlpatterns = [
    path('<str:refn>/', get_or_create_discussion, name='get_or_create_discussion'),
    path('', get_all_discussions, name='get_all_discussions'),
]
