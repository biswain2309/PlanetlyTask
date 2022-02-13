from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions


schema_view = get_schema_view(
    openapi.Info(
        title="Planetly Task API",
        default_version='v1',
        description="API Docs",
        terms_of_service="https://www.testtask.com/policies/terms/",
        contact=openapi.Contact(email="contact@test.local"),
        license=openapi.License(name="TEST License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# schema_view = get_schema_view(title='Users Usage API', renderer_classes=[OpenAPIRenderer, SwaggerUIRenderer])

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('auth.urls')),
    path('api/v1/', include('app.urls')),
    path('', schema_view.with_ui('swagger', cache_timeout=None), name='schema-swagger-ui'),
]
