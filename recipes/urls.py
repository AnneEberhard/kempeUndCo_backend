from django.urls import path
from .views import RecipeCreateView, RecipeDetailView, RecipeListView

urlpatterns = [
    path('create/', RecipeCreateView.as_view(), name='recipe-create'),  
    path('<int:pk>/', RecipeDetailView.as_view(), name='recipe-detail'),
    path('', RecipeListView.as_view(), name='recipe-list'),
]
