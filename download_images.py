import os
import django
import urllib.request
import random
from pathlib import Path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.products.models import Category, Product, ProductImage


def download_image(url, filepath):
    """Download image from URL"""
    try:
        urllib.request.urlretrieve(url, filepath)
        print(f"  Downloaded: {os.path.basename(filepath)}")
        return True
    except Exception as e:
        print(f"  Error: {e}")
        return False


def download_sample_images():
    print("=" * 50)
    print("DOWNLOADING SAMPLE IMAGES")
    print("=" * 50)
    
    media_path = '/app/media'
    products_path = os.path.join(media_path, 'products')
    categories_path = os.path.join(media_path, 'categories')
    
    os.makedirs(products_path, exist_ok=True)
    os.makedirs(categories_path, exist_ok=True)
    
    print("\n1. Downloading category images...")
    categories = Category.objects.filter(parent__isnull=True)
    category_images = {
        'Electronica': 0,
        'Ropa': 65,
        'Hogar': 35,
        'Deportes': 26,
        'Libros': 24,
    }
    
    for cat in categories:
        image_id = category_images.get(cat.name, 0)
        url = f"https://picsum.photos/id/{image_id}/800/600"
        filename = f"category_{cat.slug}.jpg"
        filepath = os.path.join(categories_path, filename)
        
        if download_image(url, filepath):
            cat.image = f"categories/{filename}"
            cat.save()
            print(f"    Category: {cat.name}")
    
    print("\n2. Downloading product images...")
    products = Product.objects.all()
    
    for i, product in enumerate(products):
        num_images = random.randint(2, 4)
        print(f"    {product.name}: {num_images} images")
        
        for j in range(num_images):
            image_id = random.randint(1, 200)
            url = f"https://picsum.photos/id/{image_id}/800/800"
            filename = f"product_{product.id}_{j+1}.jpg"
            filepath = os.path.join(products_path, filename)
            
            if download_image(url, filepath):
                img = ProductImage.objects.create(
                    image=f"products/{filename}",
                    alt_text=f"{product.name} - Imagen {j+1}",
                    is_primary=(j == 0)
                )
                product.images.add(img)
    
    print("\n" + "=" * 50)
    print("IMAGES DOWNLOADED SUCCESSFULLY!")
    print("=" * 50)
    print(f"Total ProductImages: {ProductImage.objects.count()}")
    print(f"Products with images: {Product.objects.filter(images__isnull=False).distinct().count()}")


if __name__ == '__main__':
    download_sample_images()
