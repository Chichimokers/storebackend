import os
import django
import random
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.products.models import Category, Product, ProductImage
from apps.users.models import User


def create_categories():
    print("Creating categories...")
    
    categorias = [
        {
            'name': 'Electronica',
            'description': 'Devices and electronics',
            'children': ['Smartphones', 'Laptops', 'Tablets', 'Accesorios']
        },
        {
            'name': 'Ropa',
            'description': 'Fashion and clothing',
            'children': ['Hombres', 'Mujeres', 'Ninos', 'Zapatos']
        },
        {
            'name': 'Hogar',
            'description': 'Home and furniture',
            'children': ['Muebles', 'Decoracion', 'Cocina', 'Dormitorio']
        },
        {
            'name': 'Deportes',
            'description': 'Sports and fitness',
            'children': ['Fitness', 'Futbol', 'Basquetbol', 'Cycling']
        },
        {
            'name': 'Libros',
            'description': 'Books and literature',
            'children': ['Novelas', 'Educativos', 'Comics', 'Revistas']
        }
    ]
    
    created = []
    for cat_data in categorias:
        parent, created_parent = Category.objects.get_or_create(
            name=cat_data['name'],
            defaults={
                'description': cat_data['description']
            }
        )
        created.append(parent)
        print(f"  - {parent.name}")
        
        for child_name in cat_data['children']:
            child, created_child = Category.objects.get_or_create(
                name=child_name,
                parent=parent
            )
            print(f"      - {child.name}")
    
    return created


def create_products():
    print("\nCreating products...")
    
    productos = [
        {'name': 'iPhone 15 Pro', 'price': 999.99, 'cat': 'Smartphones', 'stock': 10},
        {'name': 'Samsung Galaxy S24', 'price': 899.99, 'cat': 'Smartphones', 'stock': 15},
        {'name': 'Google Pixel 8', 'price': 699.99, 'cat': 'Smartphones', 'stock': 8},
        {'name': 'MacBook Pro 14"', 'price': 1999.99, 'cat': 'Laptops', 'stock': 5},
        {'name': 'Dell XPS 15', 'price': 1499.99, 'cat': 'Laptops', 'stock': 7},
        {'name': 'ThinkPad X1 Carbon', 'price': 1299.99, 'cat': 'Laptops', 'stock': 6},
        {'name': 'iPad Pro 12.9"', 'price': 1099.99, 'cat': 'Tablets', 'stock': 12},
        {'name': 'Samsung Tab S9', 'price': 849.99, 'cat': 'Tablets', 'stock': 9},
        
        {'name': 'Camiseta Básica', 'price': 19.99, 'cat': 'Hombres', 'stock': 50},
        {'name': 'Jeans Slim', 'price': 49.99, 'cat': 'Hombres', 'stock': 30},
        {'name': 'Chaqueta de Cuero', 'price': 149.99, 'cat': 'Hombres', 'stock': 15},
        {'name': 'Vestido Elegante', 'price': 79.99, 'cat': 'Mujeres', 'stock': 25},
        {'name': 'Blusa de Seda', 'price': 39.99, 'cat': 'Mujeres', 'stock': 20},
        {'name': 'Falda Corta', 'price': 29.99, 'cat': 'Mujeres', 'stock': 18},
        {'name': 'Zapatillas Running', 'price': 89.99, 'cat': 'Zapatos', 'stock': 40},
        {'name': 'Botas de Cuero', 'price': 119.99, 'cat': 'Zapatos', 'stock': 22},
        
        {'name': 'Sofá 3 Plazas', 'price': 599.99, 'cat': 'Muebles', 'stock': 8},
        {'name': 'Mesa de Centro', 'price': 199.99, 'cat': 'Muebles', 'stock': 12},
        {'name': 'Silla Gamer', 'price': 299.99, 'cat': 'Muebles', 'stock': 10},
        {'name': 'Lámpara de Pie', 'price': 49.99, 'cat': 'Decoración', 'stock': 25},
        {'name': 'Marco de Fotos', 'price': 15.99, 'cat': 'Decoración', 'stock': 60},
        {'name': 'Juego de Ollas', 'price': 89.99, 'cat': 'Cocina', 'stock': 15},
        {'name': 'Batidora Profesional', 'price': 69.99, 'cat': 'Cocina', 'stock': 20},
        {'name': 'Juego de Sábanas', 'price': 39.99, 'cat': 'Dormitorio', 'stock': 35},
        
        {'name': 'Mancuernas 10kg', 'price': 29.99, 'cat': 'Fitness', 'stock': 50},
        {'name': 'Esterilla de Yoga', 'price': 19.99, 'cat': 'Fitness', 'stock': 40},
        {'name': 'Bola de Ejercicio', 'price': 15.99, 'cat': 'Fitness', 'stock': 30},
        {'name': 'Balón de Fútbol', 'price': 24.99, 'cat': 'Fútbol', 'stock': 45},
        {'name': 'Guantes de Portero', 'price': 34.99, 'cat': 'Fútbol', 'stock': 20},
        {'name': 'Balón de Básquetbol', 'price': 29.99, 'cat': 'Básquetbol', 'stock': 25},
        {'name': 'Bicicleta Estática', 'price': 399.99, 'cat': 'Cycling', 'stock': 8},
        {'name': 'Casco de Ciclismo', 'price': 49.99, 'cat': 'Cycling', 'stock': 30},
        
        {'name': 'El Principito', 'price': 12.99, 'cat': 'Novelas', 'stock': 100},
        {'name': 'Cien Años de Soledad', 'price': 15.99, 'cat': 'Novelas', 'stock': 80},
        {'name': 'Harry Potter Pack', 'price': 49.99, 'cat': 'Novelas', 'stock': 50},
        {'name': 'Matemáticas Avanzadas', 'price': 39.99, 'cat': 'Educativos', 'stock': 30},
        {'name': 'Aprende Python', 'price': 24.99, 'cat': 'Educativos', 'stock': 45},
        {'name': 'Batman Comic #1', 'price': 9.99, 'cat': 'Comics', 'stock': 200},
        {'name': 'Spider-Man Comic', 'price': 9.99, 'cat': 'Comics', 'stock': 180},
        {'name': 'Revista Tech', 'price': 5.99, 'cat': 'Revistas', 'stock': 100},
    ]
    
    for prod in productos:
        category = Category.objects.filter(name=prod['cat']).first()
        if category:
            product, created = Product.objects.get_or_create(
                name=prod['name'],
                defaults={
                    'description': f'High quality {prod["name"]} for sale. Best price in the market.',
                    'price': Decimal(str(prod['price'])),
                    'compare_price': Decimal(str(prod['price'] * 1.2)),
                    'stock': prod['stock'],
                    'category': category,
                    'is_active': True
                }
            )
            if created:
                print(f"  - {product.name} (${product.price})")
    
    print(f"\nTotal products: {Product.objects.count()}")


def create_sample_users():
    print("\nCreating sample users...")
    
    users_data = [
        {'email': 'admin@admin.com', 'username': 'admin', 'first_name': 'Admin', 'last_name': 'User'},
        {'email': 'cliente@test.com', 'username': 'cliente', 'first_name': 'Juan', 'last_name': 'Pérez'},
    ]
    
    for user_data in users_data:
        if not User.objects.filter(email=user_data['email']).exists():
            user = User.objects.create_user(
                email=user_data['email'],
                username=user_data['username'],
                password='password123',
                first_name=user_data['first_name'],
                last_name=user_data['last_name']
            )
            print(f"  - {user.email} (password: password123)")


def populate():
    print("=" * 50)
    print("POPULATING DATABASE")
    print("=" * 50)
    
    create_categories()
    create_products()
    create_sample_users()
    
    print("\n" + "=" * 50)
    print("DATABASE POPULATED SUCCESSFULLY!")
    print("=" * 50)
    print(f"\nCategories: {Category.objects.count()}")
    print(f"Products: {Product.objects.count()}")
    print(f"Users: {User.objects.count()}")


if __name__ == '__main__':
    populate()
