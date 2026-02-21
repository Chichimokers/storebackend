import os
import django
import urllib.request
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.products.models import Category, Product, ProductImage


def download_image(url, filename):
    """Download image from URL and save to media/products/"""
    media_path = '/app/media/products'
    os.makedirs(media_path, exist_ok=True)
    
    filepath = os.path.join(media_path, filename)
    
    try:
        urllib.request.urlretrieve(url, filepath)
        print(f"Downloaded: {filename}")
        return filepath
    except Exception as e:
        print(f"Error downloading {filename}: {e}")
        return None


def download_sample_images():
    print("Downloading sample images for products...")
    
    products = Product.objects.all()[:20]
    
    for i, product in enumerate(products):
        # Use Picsum for random images
        image_id = random.randint(1, 1000)
        url = f"https://picsum.photos/id/{image_id}/800/800"
        filename = f"product_{product.id}.jpg"
        
        filepath = download_image(url, filename)
        
        if filepath:
            # Create ProductImage
            img = ProductImage.objects.create(
                image=f"products/{filename}",
                alt_text=product.name,
                is_primary=(i == 0)
            )
            product.images.add(img)
            print(f"  Added image to: {product.name}")
    
    print(f"\nTotal images downloaded: {ProductImage.objects.count()}")


def download_category_images():
    print("\nDownloading sample images for categories...")
    
    categories = Category.objects.filter(parent__isnull=True)
    
    category_images = {
        'Electronica': 'https://picsum.photos/id/0/800/600',
        'Ropa': 'https://picsum.photos/id/65/800/600',
        'Hogar': 'https://picsum.photos/id/35/800/600',
        'Deportes': 'https://picsum.photos/id/26/800/600',
        'Libros': 'https://picsum.photos/id/24/800/600',
    }
    
    for cat in categories:
        if cat.name in category_images:
            url = category_images[cat.name]
            filename = f"category_{cat.slug}.jpg"
            
            filepath = download_image(url, filename)
            
            if filepath:
                cat.image = f"categories/{filename}"
                cat.save()
                print(f"  Added image to: {cat.name}")


if __name__ == '__main__':
    print("=" * 50)
    print("DOWNLOADING SAMPLE IMAGES")
    print("=" * 50)
    
    download_category_images()
    download_sample_images()
    
    print("\n" + "=" * 50)
    print("IMAGES DOWNLOADED SUCCESSFULLY!")
    print("=" * 50)
