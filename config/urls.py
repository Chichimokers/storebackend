"""
Main URL configuration for Store Backend.
"""

from django.contrib import admin
from django.urls import path, include, re_path
from django.http import JsonResponse
from django.views.static import serve
from django.conf import settings


def health_check(request):
    """Health check endpoint."""
    return JsonResponse({'status': 'ok', 'service': 'Store Backend'})


def api_root(request):
    """API root endpoint with available endpoints info."""
    return JsonResponse({
        'service': 'Store Backend API',
        'version': '1.0.0',
        'endpoints': {
            'auth': {
                'register': 'POST /api/v1/users/register/',
                'login': 'POST /api/v1/users/login/',
                'refresh': 'POST /api/v1/users/token/refresh/',
                'profile': 'GET /api/v1/users/profile/',
            },
            'products': {
                'list': 'GET /api/v1/products/',
                'categories': 'GET /api/v1/products/categories/',
            },
            'orders': {
                'create': 'POST /api/v1/orders/',
                'checkout': 'POST /api/v1/orders/checkout/',
                'list': 'GET /api/v1/orders/',
            },
        }
    })


urlpatterns = [
    path('health/', health_check, name='health-check'),
    path('api/', api_root, name='api-root'),
    path('api/v1/users/', include('apps.users.urls')),
    path('api/v1/products/', include('apps.products.urls')),
    path('api/v1/orders/', include('apps.orders.urls')),
    path('api/v1/admin/', admin.site.urls),
]

# Serve static and media files always (both DEBUG=True and DEBUG=False)
urlpatterns += [
    re_path(r'^api/v1/static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
    re_path(r'^api/v1/media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]

admin.site.site_header = 'Store Backend'
admin.site.site_title = 'Store Admin'
admin.site.index_title = 'Panel de Administración'
