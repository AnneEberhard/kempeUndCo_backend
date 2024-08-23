from django.urls import path
from .views import InfoCreateView, InfoDetailView, InfoListView, delete_image

urlpatterns = [
    path('create/', InfoCreateView.as_view(), name='create_Info'),  
    path('<int:info_id>/delete-image/<str:image_field>/', delete_image, name='delete_image'),
    path('<int:pk>/', InfoDetailView.as_view(), name='info-detail'),
    
    path('', InfoListView.as_view(), name='info-list'),
]
