from rest_framework import serializers
from .models import Category, Product, ProductImage


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'alt_text', 'is_primary']


class CategorySerializer(serializers.ModelSerializer):
    subcategories = serializers.SerializerMethodField()
    products_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'image', 'parent', 'subcategories', 'products_count', 'is_active', 'created_at']

    def get_subcategories(self, obj):
        if obj.parent is None:
            subcategories = Category.objects.filter(parent=obj)
            return CategorySerializer(subcategories, many=True).data
        return []

    def get_products_count(self, obj):
        return obj.products.filter(is_active=True).count()


class CategorySimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']


class ProductListSerializer(serializers.ModelSerializer):
    category = CategorySimpleSerializer(read_only=True)
    main_image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'slug', 'description', 'price', 'compare_price', 'stock', 'category', 'main_image', 'is_active', 'created_at']

    def get_main_image(self, obj):
        img = obj.main_image
        if img:
            return ProductImageSerializer(img).data
        return None


class ProductDetailSerializer(serializers.ModelSerializer):
    category = CategorySimpleSerializer(read_only=True)
    subcategory = CategorySimpleSerializer(read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'description', 'price', 'compare_price', 'stock',
            'category', 'subcategory', 'images', 'is_active', 'created_at', 'updated_at'
        ]


class ProductCreateUpdateSerializer(serializers.ModelSerializer):
    image_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )

    class Meta:
        model = Product
        fields = [
            'name', 'description', 'price', 'compare_price', 'stock',
            'category', 'subcategory', 'image_ids', 'is_active'
        ]

    def create(self, validated_data):
        image_ids = validated_data.pop('image_ids', [])
        product = Product.objects.create(**validated_data)
        if image_ids:
            images = ProductImage.objects.filter(id__in=image_ids)
            product.images.set(images)
        return product

    def update(self, instance, validated_data):
        image_ids = validated_data.pop('image_ids', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if image_ids is not None:
            images = ProductImage.objects.filter(id__in=image_ids)
            instance.images.set(images)
        return instance
