# API de Administración - Endpoints Masters

**Base URL:** `https://tu-dominio.com/api/v1/`

**Header requerido:**
```
Authorization: Bearer <token_admin>
```

---

## Endpoints de Admin

| Recurso | Métodos | Endpoint |
|---------|---------|----------|
| **Dashboard** | GET | `/api/v1/admin/dashboard/` |
| **Usuarios** | GET, POST | `/api/v1/admin/users/` |
| **Usuario (detalle)** | GET, PUT, DELETE | `/api/v1/admin/users/{id}/` |
| **Órdenes (todas)** | GET | `/api/v1/admin/all-orders/` |
| **Orden (detalle)** | GET, PATCH, DELETE | `/api/v1/admin/all-orders/{id}/` |
| **Productos** | GET, POST | `/api/v1/admin/products/` |
| **Producto (detalle)** | GET, PUT, DELETE | `/api/v1/admin/products/{id}/` |
| **Categorías** | GET, POST | `/api/v1/admin/categories/` |
| **Categoría (detalle)** | GET, PUT, DELETE | `/api/v1/admin/categories/{id}/` |
| **Imágenes** | GET, POST, DELETE | `/api/v1/admin/product-images/` |

---

## 1. Dashboard

### GET /api/v1/admin/dashboard/
Retorna estadísticas del sistema.

**Response:**
```json
{
    "orders": {
        "total": 100,
        "pending": 5,
        "processing": 2,
        "completed": 80,
        "cancelled": 13
    },
    "products": {
        "total": 50,
        "active": 45
    },
    "users": {
        "total": 25
    },
    "revenue": "15000.00"
}
```

---

## 2. Usuarios

### Listar usuarios
```
GET /api/v1/admin/users/
Query params: ?search=email&ordering=-created_at
```

**Response:**
```json
{
    "count": 25,
    "results": [
        {
            "id": 1,
            "email": "admin@admin.com",
            "username": "admin",
            "first_name": "Admin",
            "last_name": "User",
            "is_staff": true,
            "is_superuser": true,
            "is_active": true,
            "created_at": "2024-01-01T00:00:00Z"
        }
    ]
}
```

### Crear usuario
```
POST /api/v1/admin/users/
{
    "email": "user@email.com",
    "username": "username",
    "password": "password123",
    "password_confirm": "password123",
    "first_name": "Juan",
    "last_name": "Pérez",
    "is_staff": false,
    "is_active": true
}
```

### Actualizar usuario
```
PUT /api/v1/admin/users/{id}/
{
    "first_name": "Nuevo nombre",
    "is_active": false
}
```

### Eliminar usuario
```
DELETE /api/v1/admin/users/{id}/
```

---

## 3. Órdenes (todas las del sistema)

### Listar todas las órdenes
```
GET /api/v1/admin/all-orders/
Query params: 
    ?status=pending
    ?search=juan
    ?ordering=-created_at
```

**Response:**
```json
{
    "count": 100,
    "results": [
        {
            "id": 1,
            "user": 1,
            "products": [
                {"id": 1, "name": "Producto", "price": "99.99", "quantity": 2, "subtotal": "199.98"}
            ],
            "total_amount": "199.98",
            "status": "pending",
            "customer_name": "Juan Pérez",
            "customer_phone": "+5351234567",
            "customer_address": "Calle 123",
            "notes": "Entregar mañana",
            "created_at": "2024-01-01T00:00:00Z"
        }
    ]
}
```

### Actualizar estado de orden
```
PATCH /api/v1/admin/all-orders/{id}/
{
    "status": "completed"  // pending, processing, completed, cancelled
}
```

### Ver orden específica
```
GET /api/v1/admin/all-orders/{id}/
```

### Eliminar orden
```
DELETE /api/v1/admin/all-orders/{id}/
```

---

## 4. Productos

### Listar productos
```
GET /api/v1/admin/products/
Query params:
    ?search=iphone
    ?category=1
    ?ordering=-created_at
```

### Crear producto
```
POST /api/v1/admin/products/
{
    "name": "Nuevo Producto",
    "description": "Descripción del producto",
    "price": 99.99,
    "compare_price": 129.99,
    "stock": 10,
    "category": 1,
    "subcategory": null,
    "is_active": true,
    "image_ids": [1, 2, 3]
}
```

### Actualizar producto
```
PUT /api/v1/admin/products/{id}/
```

### Eliminar producto
```
DELETE /api/v1/admin/products/{id}/
```

---

## 5. Categorías

### Listar categorías
```
GET /api/v1/admin/categories/
```

### Crear categoría
```
POST /api/v1/admin/categories/
{
    "name": "Nueva Categoría",
    "description": "Descripción",
    "parent": null,
    "is_active": true
}
```

- `parent`: ID de categoría padre (null para raíz)

### Actualizar/Eliminar
```
PUT /api/v1/admin/categories/{id}/
DELETE /api/v1/admin/categories/{id}/
```

---

## 6. Imágenes

### Subir imagen
```
POST /api/v1/admin/product-images/
Content-Type: multipart/form-data
Body: image=archivo
```

**Response:**
```json
{
    "id": 1,
    "image": "/api/v1/media/products/img.jpg",
    "alt_text": "",
    "is_primary": false
}
```

### Listar imágenes
```
GET /api/v1/admin/product-images/
```

### Eliminar imagen
```
DELETE /api/v1/admin/product-images/{id}/
```

---

## Autenticación

### Login
```
POST /api/v1/users/login/
{
    "email": "admin@admin.com",
    "password": "admin123"
}
```

El token se usa en los headers:
```
Authorization: Bearer <token>
```

---

## Ejemplo: Uso desde Frontend

```javascript
const API = 'https://tu-dominio.com/api/v1';
const token = localStorage.getItem('access_token');

const headers = {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
};

// 1. Dashboard
const dash = await fetch(`${API}/admin/dashboard/`, { headers });
const stats = await dash.json();

// 2. Todas las órdenes
const orders = await fetch(`${API}/admin/all-orders/`, { headers });
const ordersData = await orders.json();

// 3. Cambiar estado
await fetch(`${API}/admin/all-orders/1/`, {
    method: 'PATCH',
    headers,
    body: JSON.stringify({ status: 'completed' })
});

// 4. Crear producto
await fetch(`${API}/admin/products/`, {
    method: 'POST',
    headers,
    body: JSON.stringify({
        name: 'Nuevo',
        price: 99.99,
        stock: 10,
        category: 1
    })
});
```
