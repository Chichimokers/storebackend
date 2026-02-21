from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'', views.OrderViewSet, basename='order')

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('', include(router.urls)),
]
