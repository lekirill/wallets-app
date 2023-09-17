from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from app.api.health_check import HealthCheckView

schema_view = get_schema_view(
    openapi.Info(
        title="WALLETS API",
        default_version="v1",
    ),
    public=True,
    permission_classes=[permissions.AllowAny, ],
)

urlpatterns = [
    path('health_check/', view=HealthCheckView.as_view(), name='health-check'),
    path('v1/', include('app.api.v1.urls')),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
