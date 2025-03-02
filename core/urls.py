import os
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from api.views import prediction_view, healthcheck
from core.utils import create_media_directory

url = os.environ.get("URL")

schema_view = get_schema_view(
    openapi.Info(
        title="Fibrosis staging",
        default_version='v1',
        description="API ",
        contact=openapi.Contact(email="esther.camilo@gntech.med.br"),
    ),
    url=url,
    public=True,
    permission_classes=[permissions.AllowAny, ],
    authentication_classes=[],
)

create_media_directory()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/predict/<model>/', prediction_view, name='prediction_view'),
    path('api/health-check/', healthcheck, name='healthcheck'),
    path('api-auth/', include('rest_framework.urls'), name='rest_framework_transaction'),
    path('api/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]

if bool(settings.DEBUG):
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
