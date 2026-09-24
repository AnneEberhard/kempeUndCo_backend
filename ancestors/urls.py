from django.urls import path
from .views import AdminPersonDetailView, AdminPersonListView, AdminRelationDetailView, PersonListCreateView, PersonDetailView, RelationListCreateView, RelationDetailView

urlpatterns = [
    path('persons/', PersonListCreateView.as_view(), name='person-list-create'),
    path('persons/<int:pk>/', PersonDetailView.as_view(), name='person-detail'),
    path('relations/', RelationListCreateView.as_view(), name='relation-list-create'),
    path('relations/<int:person_id>/', RelationDetailView.as_view(), name='relation-detail'),
    path('admin/persons/<path:refn>/', AdminPersonDetailView.as_view(), name='admin-person-detail'),
    path('admin/persons/', AdminPersonListView.as_view(), name='admin-person-list'),
    path('admin/relations/<path:refn>/', AdminRelationDetailView.as_view(), name='admin-relation-detail'),
]
