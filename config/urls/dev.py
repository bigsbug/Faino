from django.urls import path, include

from config.urls.base import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.views import (
    SpectacularSwaggerView,
    SpectacularRedocView,
    SpectacularAPIView,
)

urls_local_apps = [
    path("", include("faino.WebServer.urls", "Device")),
    path("api/", include("faino.API.urls", "API")),
]

urls_third_party_apps = [
    path("__debug__/", include("debug_toolbar.urls")),
    path("api/token/", TokenObtainPairView.as_view(), name="token_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_pair_refresh"),
    # path("api/token/verify/", TokenVerifyView.as_view(), name="token_pair_verify"),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
]

urlpatterns += urls_local_apps + urls_third_party_apps
