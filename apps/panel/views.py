from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from django.db.models import Sum, Count

from apps.users.models import User
from apps.orders.models import Order
from apps.products.models import Product, Category
from apps.users.serializers import UserSerializer
from apps.orders.serializers import OrderSerializer


class AdminUserViewSet(viewsets.ModelViewSet):
    """ViewSet para gestión de usuarios (solo admin)"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
    search_fields = ['email', 'username', 'first_name', 'last_name']
    ordering_fields = ['id', 'email', 'created_at']


class AdminOrderViewSet(viewsets.ModelViewSet):
    """ViewSet para gestión de órdenes (solo admin) - todas las órdenes"""
    queryset = Order.objects.all().order_by('-created_at')
    serializer_class = OrderSerializer
    permission_classes = [IsAdminUser]
    filterset_fields = ['status']
    search_fields = ['customer_name', 'customer_phone', 'user__email']
    ordering_fields = ['created_at', 'total_amount', 'status']

    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        """Actualizar estado de orden"""
        order = self.get_object()
        new_status = request.data.get('status')
        if new_status in ['pending', 'processing', 'completed', 'cancelled']:
            order.status = new_status
            order.save()
            return Response({'message': f'Order status updated to {new_status}'})
        return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def dashboard(request):
    """Dashboard con estadísticas"""
    total_orders = Order.objects.count()
    pending_orders = Order.objects.filter(status='pending').count()
    processing_orders = Order.objects.filter(status='processing').count()
    completed_orders = Order.objects.filter(status='completed').count()
    cancelled_orders = Order.objects.filter(status='cancelled').count()
    
    total_products = Product.objects.count()
    active_products = Product.objects.filter(is_active=True).count()
    
    total_users = User.objects.count()
    
    revenue = Order.objects.filter(status='completed').aggregate(total=Sum('total_amount'))['total'] or 0
    
    return Response({
        'orders': {
            'total': total_orders,
            'pending': pending_orders,
            'processing': processing_orders,
            'completed': completed_orders,
            'cancelled': cancelled_orders,
        },
        'products': {
            'total': total_products,
            'active': active_products,
        },
        'users': {
            'total': total_users,
        },
        'revenue': str(revenue),
    })
