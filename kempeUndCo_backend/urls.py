"""
URL configuration for kempeUndCo_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/discussions/', include('discussions.urls')),
    path('api/ancestors/', include('ancestors.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
