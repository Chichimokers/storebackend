from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.conf import settings
from urllib.parse import quote

from apps.products.models import Product
from .models import Order
from .serializers import OrderSerializer, OrderCreateSerializer, OrderCheckoutSerializer


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = OrderCreateSerializer(data=request.data)
        if serializer.is_valid():
            products_data = serializer.validated_data['products']
            
            products_list = []
            total = 0
            
            for item in products_data:
                try:
                    product = Product.objects.get(id=item['id'], is_active=True)
                except Product.DoesNotExist:
                    return Response(
                        {'error': f'Product with id {item["id"]} not found'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                quantity = item['quantity']
                subtotal = product.price * quantity
                total += subtotal
                
                products_list.append({
                    'id': product.id,
                    'name': product.name,
                    'price': str(product.price),
                    'quantity': quantity,
                    'subtotal': str(subtotal)
                })
            
            order = Order.objects.create(
                user=request.user,
                products=products_list,
                total_amount=total,
                customer_name=serializer.validated_data['customer_name'],
                customer_phone=serializer.validated_data['customer_phone'],
                customer_address=serializer.validated_data.get('customer_address', ''),
                notes=serializer.validated_data.get('notes', '')
            )
            
            return Response(
                OrderSerializer(order).data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def checkout(request):
    serializer = OrderCheckoutSerializer(data=request.data)
    if serializer.is_valid():
        products_data = serializer.validated_data['products']
        
        products_list = []
        total = 0
        message_parts = []
        
        for item in products_data:
            try:
                product = Product.objects.get(id=item['id'], is_active=True)
            except Product.DoesNotExist:
                return Response(
                    {'error': f'Product with id {item["id"]} not found'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            quantity = item['quantity']
            if quantity > product.stock:
                return Response(
                    {'error': f'Not enough stock for {product.name}. Available: {product.stock}'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            subtotal = product.price * quantity
            total += subtotal
            
            products_list.append({
                'id': product.id,
                'name': product.name,
                'price': str(product.price),
                'quantity': quantity,
                'subtotal': str(subtotal)
            })
            
            message_parts.append(f"- {product.name} x{quantity} = ${subtotal}")
        
        customer_name = serializer.validated_data['customer_name']
        
        message = f"Hola, mi nombre es {customer_name}. Quiero comprar:\n\n"
        message += "\n".join(message_parts)
        message += f"\n\nTotal: ${total}"
        
        order = Order.objects.create(
            user=request.user,
            products=products_list,
            total_amount=total,
            status='pending',
            customer_name=customer_name,
            customer_phone=serializer.validated_data['customer_phone'],
            customer_address=serializer.validated_data.get('customer_address', ''),
            notes=serializer.validated_data.get('notes', '')
        )
        
        whatsapp_phone = settings.WHATSAPP_PHONE
        encoded_message = quote(message)
        whatsapp_url = f"https://wa.me/{whatsapp_phone.replace('+', '')}?text={encoded_message}"
        
        return Response({
            'order_id': order.id,
            'phone': whatsapp_phone,
            'message': message,
            'whatsapp_url': whatsapp_url,
            'order_total': str(total)
        })
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
