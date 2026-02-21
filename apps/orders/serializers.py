from rest_framework import serializers
from django.conf import settings
from .models import Order


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            'id', 'user', 'products', 'total_amount', 'status',
            'customer_name', 'customer_phone', 'customer_address',
            'notes', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'total_amount', 'status', 'created_at', 'updated_at']


class OrderCreateSerializer(serializers.Serializer):
    products = serializers.ListField(
        child=serializers.DictField(
            child=serializers.IntegerField()
        ),
        min_length=1
    )
    customer_name = serializers.CharField(max_length=200)
    customer_phone = serializers.CharField(max_length=20)
    customer_address = serializers.CharField(required=False, allow_blank=True, default='')
    notes = serializers.CharField(required=False, allow_blank=True, default='')

    def validate_products(self, value):
        if not value:
            raise serializers.ValidationError('Products list cannot be empty')
        
        for item in value:
            if 'id' not in item or 'quantity' not in item:
                raise serializers.ValidationError('Each product must have id and quantity')
            if item['quantity'] < 1:
                raise serializers.ValidationError('Quantity must be at least 1')
        
        return value


class OrderCheckoutSerializer(serializers.Serializer):
    products = serializers.ListField(
        child=serializers.DictField(
            child=serializers.IntegerField()
        ),
        min_length=1
    )
    customer_name = serializers.CharField(max_length=200)
    customer_phone = serializers.CharField(max_length=20)

    def validate_products(self, value):
        if not value:
            raise serializers.ValidationError('Products list cannot be empty')
        
        for item in value:
            if 'id' not in item or 'quantity' not in item:
                raise serializers.ValidationError('Each product must have id and quantity')
            if item['quantity'] < 1:
                raise serializers.ValidationError('Quantity must be at least 1')
        
        return value
