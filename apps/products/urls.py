from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'categories', views.CategoryViewSet, basename='category')
router.register(r'', views.ProductViewSet, basename='product')

urlpatterns = [
    path('images/', views.ProductImageViewSet.as_view({'get': 'list', 'post': 'create'}), name='product-images'),
    path('', include(router.urls)),
]
