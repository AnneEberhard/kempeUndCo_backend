from django.urls import path
from .views import InfoCreateView, InfoDetailView, InfoListView, delete_image

urlpatterns = [
    path('create/', InfoCreateView.as_view(), name='create_Info'),  
    path('<int:pk>/', InfoDetailView.as_view(), name='info-detail'),
    path('', InfoListView.as_view(), name='info-list'),
]
