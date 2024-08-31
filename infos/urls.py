from django.urls import path
from .views import InfoCreateView, InfoDetailView, InfoListView

urlpatterns = [
    path('create/', InfoCreateView.as_view(), name='info-create'),
    path('<int:pk>/', InfoDetailView.as_view(), name='info-detail'),
    path('', InfoListView.as_view(), name='info-list'),
]
