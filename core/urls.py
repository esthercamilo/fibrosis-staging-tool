import os
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from api.views import QuestionView, StudentView
from core.utils import create_media_directory
from rest_framework.authtoken.views import obtain_auth_token

url = os.environ.get("URL")

schema_view = get_schema_view(
    openapi.Info(
        title="Via Intensiva",
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

    path('api/question/<question_id>', QuestionView.as_view({'get': 'get'}), name='question_get_view'),
    path('api/question/create/', QuestionView.as_view({'post': 'post'}), name='question_update_view'),
    path('api/question/update/<question_id>/', QuestionView.as_view({'put': 'put'}), name='question_create_view'),
    path('api/question/delete/<question_id>/', QuestionView.as_view({'delete': 'delete'}), name='question_delete_view'),
    path('api/question/show_all/', QuestionView.as_view({'get': 'show_all'}), name='question_show_all_view'),

    path('api/student/<student_id>', StudentView.as_view({'get': 'get'}), name='student_get_view'),
    path('api/student/signup/', StudentView.as_view({'post': 'post'}), name='student_post_view'),
    path('api/student/update/<student_id>/', StudentView.as_view({'put': 'put'}), name='student_update_view'),
    path('api/student/filter', StudentView.as_view({'get': 'filter'}), name='student_filter_view'),
    path('api/student/delete/<student_id>', StudentView.as_view({'delete': 'delete'}), name='student_delete_view'),
    #mostra todos os estudantes

    path('api-auth/', include('rest_framework.urls'), name='rest_framework_transaction'),
    path('api/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),


]

if bool(settings.DEBUG):
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
