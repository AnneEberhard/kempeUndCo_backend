"""
URL configuration for kempeUndCo_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static

from accounts.views import ActivationView, BlacklistTokenView, ChangeAuthorNameView, ChangePasswordView, LoginView, PasswordResetConfirmView, PasswordResetRequestView, RegistrationView
from rest_framework_simplejwt.views import TokenRefreshView

from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="KempeUndCo",
        default_version='v1',
        description="API documentation for KempeUndCo",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@yourproject.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(), name='login'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegistrationView.as_view(), name='register'),
    path('activate/<uidb64>/<token>/', ActivationView.as_view(), name='activate'),
    path('token/blacklist/', BlacklistTokenView.as_view(), name='token_blacklist'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('change-name/', ChangeAuthorNameView.as_view(), name='change-name'),
    path('password-reset-request/', PasswordResetRequestView.as_view(), name='password_reset_request'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('api/discussions/', include('discussions.urls')),
    path('api/ancestors/', include('ancestors.urls')),
    path('api/infos/', include('infos.urls')),
    path('api/fam-infos/', include('famInfos.urls')),
    path('api/recipes/', include('recipes.urls')),
    path('api/comments/', include('comments.urls')),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
