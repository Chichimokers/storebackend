# Documentación API - Panel de Administración

## Base URL
```
https://tu-dominio.com/api/v1/
```

## Autenticación

### Login
```
POST /api/v1/users/login/
Content-Type: application/json

Request:
{
    "email": "admin@admin.com",
    "password": "admin123"
}

Response (200):
{
    "user": {
        "id": 1,
        "email": "admin@admin.com",
        "username": "admin",
        "first_name": "Admin",
        "last_name": "User",
        "is_staff": true,
        "is_superuser": true,
        "is_active": true,
        "created_at": "2024-01-01T00:00:00Z"
    },
    "tokens": {
        "refresh": "eyJ...",
        "access": "eyJ..."
    }
}
```

### Cómo saber si el usuario es Admin

En el **login** o al obtener el **perfil**, el objeto `user` contiene los campos:
- `is_staff`: true/false - Puede acceder al admin
- `is_superuser`: true/false - Es superusuario

```javascript
// Después del login
const response = await fetch('/api/v1/users/login/', {...});
const { user } = await response.json();

if (user.is_staff || user.is_superuser) {
    // Mostrar panel de admin
    showAdminPanel();
} else {
    // Solo usuario normal
    showRegularUI();
}

// Obtener perfil actual
const profileRes = await fetch('/api/v1/users/profile/', {
    headers: {'Authorization': `Bearer ${token}`}
});
const profile = await profileRes.json();
const isAdmin = profile.is_staff;
```

**Headers requeridos:**
```
Authorization: Bearer <access_token>
```

---

## Endpoints Disponibles

### USUARIOS

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/v1/users/profile/` | Ver mi perfil |
| PUT | `/api/v1/users/profile/` | Actualizar mi perfil |
| POST | `/api/v1/users/change-password/` | Cambiar mi contraseña |

---

### PRODUCTOS

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/v1/products/` | Listar productos (paginado) |
| GET | `/api/v1/products/{id}/` | Ver producto específico |
| POST | `/api/v1/products/` | Crear producto |
| PUT | `/api/v1/products/{id}/` | Actualizar producto |
| DELETE | `/api/v1/products/{id}/` | Eliminar producto |
| GET | `/api/v1/products/featured/` | Productos destacados |
| GET | `/api/v1/products/?search=query` | Buscar productos |
| GET | `/api/v1/products/?category=1` | Filtrar por categoría |

#### Estructura Producto (Request POST/PUT)
```json
{
    "name": "Nombre del producto",
    "description": "Descripción",
    "price": 99.99,
    "compare_price": 129.99,
    "stock": 10,
    "category": 1,
    "subcategory": null,
    "is_active": true,
    "image_ids": [1, 2, 3]
}
```

---

### CATEGORÍAS

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/v1/products/categories/` | Listar categorías |
| GET | `/api/v1/products/categories/{id}/` | Ver categoría |
| POST | `/api/v1/products/categories/` | Crear categoría |
| PUT | `/api/v1/products/categories/{id}/` | Actualizar categoría |
| DELETE | `/api/v1/products/categories/{id}/` | Eliminar categoría |
| GET | `/api/v1/products/categories/{id}/subcategories/` | Subcategorías |

#### Estructura Categoría (Request POST/PUT)
```json
{
    "name": "Electrónica",
    "description": "Descripción",
    "parent": null,
    "is_active": true
}
```
- `parent`: ID de categoría padre (null para categorías raíz)

---

### IMÁGENES DE PRODUCTOS

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/v1/products/images/` | Listar todas las imágenes |
| POST | `/api/v1/products/images/` | Subir imagen |
| DELETE | `/api/v1/products/images/{id}/` | Eliminar imagen |

#### Subir Imagen
```
POST /api/v1/products/images/
Content-Type: multipart/form-data
Authorization: Bearer <token>

Body:
- image: archivo (required)
- alt_text: texto alternativo (optional)
- is_primary: true/false (optional)

Response (201):
{
    "id": 1,
    "image": "/api/v1/media/products/imagen.jpg",
    "alt_text": "iPhone 15",
    "is_primary": true
}
```

**Nota**: Para associate images a un producto, usar `image_ids` al crear/actualizar el producto.

---

### ÓRDENES

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/v1/orders/` | Mis órdenes (usuario) |
| GET | `/api/v1/orders/{id}/` | Ver orden específica |
| POST | `/api/v1/orders/` | Crear orden (registrada) |
| POST | `/api/v1/orders/checkout/` | Checkout → WhatsApp |

**Para admin**: Usar Django Admin en `/api/v1/admin/`

#### Actualizar Estado de Orden (PATCH)
```
PATCH /api/v1/orders/{id}/
Authorization: Bearer <token>
Content-Type: application/json

{
    "status": "completed"
}
```

Estados: `pending`, `processing`, `completed`, `cancelled`

---

### DASHBOARD / ADMIN

Para acceder usar Django Admin integrado:
```
/api/v1/admin/
```

**Credenciales**: usuario admin creado en el sistema

---

## Parámetros de Query

### Paginación
```
GET /api/v1/products/?page=2
```

### Búsqueda
```
GET /api/v1/products/?search=iphone
GET /api/v1/products/categories/?search=ropa
```

### Ordenamiento
```
GET /api/v1/products/?ordering=price        # menor a mayor
GET /api/v1/products/?ordering=-price       # mayor a menor
GET /api/v1/products/?ordering=name
GET /api/v1/products/?ordering=-created_at  # más recientes
```

### Filtrado
```
GET /api/v1/products/?category=1
GET /api/v1/products/?category=1&subcategory=2
```

---

## Imágenes

Las imágenes se sirven desde:
```
/api/v1/media/products/nombre-imagen.jpg
/api/v1/media/categories/nombre-imagen.jpg
```

**Nota**: Concatenar con el dominio base, ej:
```
https://inventory.cloudns.be/api/v1/media/products/imagen.jpg
```

---

## Códigos de Estado HTTP

| Código | Significado |
|--------|-------------|
| 200 | OK |
| 201 | Creado |
| 400 | Bad Request |
| 401 | No autorizado |
| 403 | Prohibido |
| 404 | No encontrado |

---

## Ejemplo: Flujo Admin

```javascript
// 1. Login
const loginRes = await fetch('/api/v1/users/login/', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
        email: 'admin@admin.com',
        password: 'admin123'
    })
});
const { tokens } = await loginRes.json();
const token = tokens.access;

// 2. Subir imagen
const formData = new FormData();
formData.append('image', fileInput.files[0]);
const imgRes = await fetch('/api/v1/products/images/', {
    method: 'POST',
    headers: {'Authorization': `Bearer ${token}`},
    body: formData
});
const { id: imageId } = await imgRes.json();

// 3. Crear producto con imagen
await fetch('/api/v1/products/', {
    method: 'POST',
    headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        name: 'Nuevo Producto',
        price: 99.99,
        stock: 10,
        category: 1,
        image_ids: [imageId]
    })
});

// 4. Listar productos
const productsRes = await fetch('/api/v1/products/', {
    headers: {'Authorization': `Bearer ${token}`}
});
const products = await productsRes.json();

// 5. Ver órdenes
const ordersRes = await fetch('/api/v1/orders/', {
    headers: {'Authorization': `Bearer ${token}`}
});
const orders = await ordersRes.json();
```

---

## Notas Importantes

1. **Imágenes**: Siempre usar `FormData` para subir
2. **Categorías**: Las subcategorías tienen `parent` = ID de la categoría padre
3. **Token**: Incluir en header `Authorization: Bearer <token>`
4. **Admin completo**: Usar Django Admin en `/api/v1/admin/`
