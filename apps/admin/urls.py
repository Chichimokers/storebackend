from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from apps.users.views import register, login, logout, profile, change_password
from apps.admin.views import AdminUserViewSet, AdminOrderViewSet, dashboard
from apps.products.views import ProductViewSet, CategoryViewSet, ProductImageViewSet

router = DefaultRouter()
router.register(r'users', AdminUserViewSet, basename='admin-user')
router.register(r'all-orders', AdminOrderViewSet, basename='admin-order')
router.register(r'products', ProductViewSet, basename='admin-product')
router.register(r'categories', CategoryViewSet, basename='admin-category')
router.register(r'product-images', ProductImageViewSet, basename='admin-product-image')

urlpatterns = [
    # Auth (público y usuario)
    path('auth/register/', register, name='register'),
    path('auth/login/', login, name='login'),
    path('auth/logout/', logout, name='logout'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/profile/', profile, name='profile'),
    path('auth/change-password/', change_password, name='change-password'),
    
    # Admin
    path('', include(router.urls)),
    path('dashboard/', dashboard, name='dashboard'),
]
