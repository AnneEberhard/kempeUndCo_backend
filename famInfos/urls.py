from django.urls import path
from .views import FamInfoCreateView, FamInfoDetailView, FamInfoListView

urlpatterns = [
    path('create/', FamInfoCreateView.as_view(), name='famInfo-create'),
    path('<int:pk>/', FamInfoDetailView.as_view(), name='famInfo-detail'),
    path('', FamInfoListView.as_view(), name='famInfo-list'),
]
