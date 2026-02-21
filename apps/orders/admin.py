from django.contrib import admin
from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'total_amount', 'status', 'customer_name', 'customer_phone', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['user__email', 'customer_name', 'customer_phone']
    readonly_fields = ['products', 'total_amount', 'created_at', 'updated_at']
    ordering = ['-created_at']
