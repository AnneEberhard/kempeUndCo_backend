from django.urls import path
from .views import get_or_create_discussion

urlpatterns = [
    path('discussion/<str:refn>/', get_or_create_discussion, name='get_or_create_discussion'),
]
