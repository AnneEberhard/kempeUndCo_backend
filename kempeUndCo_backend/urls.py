"""
URL configuration for kempeUndCo_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from accounts.views import ActivationView, LoginView, PasswordResetConfirmView, PasswordResetRequestView, RegistrationView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(), name='login'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegistrationView.as_view(), name='register'),
    path('activate/<uidb64>/<token>/', ActivationView.as_view(), name='activate'),
    path('password-reset-request/', PasswordResetRequestView.as_view(), name='password_reset_request'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('api/discussions/', include('discussions.urls')),
    path('api/ancestors/', include('ancestors.urls')),
    path('api/infos/', include('infos.urls')),
    path('api/recipes/', include('recipes.urls')),
    path('api/comments/', include('comments.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
