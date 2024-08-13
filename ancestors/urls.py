from django.urls import path
from .views import PersonListCreateView, PersonDetailView, RelationListCreateView, RelationDetailView

urlpatterns = [
    path('persons/', PersonListCreateView.as_view(), name='person-list-create'),
    path('persons/<int:pk>/', PersonDetailView.as_view(), name='person-detail'),
    path('relations/', RelationListCreateView.as_view(), name='relation-list-create'),
    path('relations/<int:person_id>/', RelationDetailView.as_view(), name='relation-detail'),
]
