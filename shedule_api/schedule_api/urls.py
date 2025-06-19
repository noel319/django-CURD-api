from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.http import JsonResponse
from django.shortcuts import render

def api_info(request):
    return JsonResponse({
        'message': 'Weekly Schedule API',
        'version': 'v1.0.0',
        'description': 'A comprehensive API for managing weekly schedules with JWT authentication',
        'documentation': {
            'swagger_ui': '/swagger/',
            'redoc': '/redoc/',
            'api_schema': '/swagger.json'
        },
        'endpoints': {
            'authentication': {
                'register': '/api/v1/auth/register/',
                'login': '/api/v1/auth/login/',
                'refresh': '/api/v1/auth/token/refresh/',
                'profile': '/api/v1/auth/profile/',
                'logout': '/api/v1/auth/logout/',
                'change_password': '/api/v1/auth/change-password/'
            },
            'schedules': {
                'list_create': '/api/v1/schedules/',
                'detail': '/api/v1/schedules/{id}/',
                'protected_demo': '/api/v1/schedules/protected/',
                'statistics': '/api/v1/schedules/statistics/'
            }
        },
        'usage': {
            'step_1': 'Register a new user account',
            'step_2': 'Login to get JWT access token',
            'step_3': 'Use token in Authorization header: Bearer <token>',
            'step_4': 'Create and manage schedules'
        }
    }, indent=2)

# Swagger schema generator
schema_view = get_schema_view(
    openapi.Info(
        title="Weekly Schedule API",
        default_version='v1',
        description="Comprehensive REST API for managing weekly schedules with JWT authentication.",
        terms_of_service="https://www.example.com/policies/terms/",
        contact=openapi.Contact(email="contact@scheduleapi.local"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

# Custom Swagger UI view (loads custom HTML)
def custom_swagger_ui(request):
    return render(request, 'swagger/swagger-ui.html', {
        'spec_url': '/swagger.json'
    })

urlpatterns = [
    path('admin/', admin.site.urls),

    # API endpoints
    path('api/v1/auth/', include('apps.authentication.urls')),
    path('api/v1/schedules/', include('apps.schedules.urls')),

    # Info endpoint
    path('api/', api_info, name='api-info'),

    # Schema definition
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),

    # Custom Swagger UI
    path('swagger/', custom_swagger_ui, name='custom-swagger-ui'),

    # Redoc (optional)
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    # Root redirect to Swagger
    path('', custom_swagger_ui),
]
