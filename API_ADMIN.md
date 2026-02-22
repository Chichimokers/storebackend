# API de Administración - Panel Admin

**Base URL:** `https://tu-dominio.com/api/v1/admin/`

**Header requerido:**
```
Authorization: Bearer <token_admin>
```

---

## ¿Qué puede hacer el usuario en cada pantalla?

### 📊 Dashboard
- Ver total de órdenes (todas las estados)
- Ver órdenes pendientes, en proceso, completadas, canceladas
- Ver total de productos y productos activos
- Ver total de usuarios registrados
- Ver ingresos totales (órdenes completadas)

### 👥 Gestión de Usuarios
- **Lista**: Ver todos los usuarios registrados
- **Crear**: Agregar nuevos usuarios (clientes o admins)
- **Editar**: Modificar datos, hacer admin, activar/desactivar
- **Eliminar**: Borrar usuarios del sistema
- **Buscar**: Por email, username, nombre

### 📦 Gestión de Órdenes
- **Lista**: Ver todas las órdenes del sistema
- **Ver detalle**: Ver productos comprados, datos del cliente
- **Cambiar estado**: pending → processing → completed / cancelled
- **Eliminar**: Borrar órdenes
- **Buscar**: Por nombre cliente, teléfono, email

### 🛍️ Gestión de Productos
- **Lista**: Ver todos los productos
- **Crear**: Agregar nuevo producto con nombre, precio, stock, categoría
- **Editar**: Modificar cualquier dato del producto
- **Activar/Desactivar**: Ocultar productos sin borrarlos
- **Eliminar**: Borrar productos permanentemente
- **Buscar**: Por nombre
- **Filtrar**: Por categoría
- **Ordenar**: Por fecha, precio, nombre

### 📂 Gestión de Categorías
- **Lista**: Ver todas las categorías y subcategorías
- **Crear**: Nueva categoría (raíz o subcategoría)
- **Editar**: Modificar nombre, descripción
- **Activar/Desactivar**: Ocultar categorías
- **Eliminar**: Borrar categorías
- **Ver subcategorías**: Ver hijos de una categoría

### 🖼️ Gestión de Imágenes
- **Subir**: Agregar nuevas imágenes al sistema
- **Lista**: Ver todas las imágenes subidas
- **Eliminar**: Borrar imágenes

---

## Endpoints Disponibles

| Recurso | Métodos | Endpoint |
|---------|---------|----------|
| **Dashboard** | GET | `/api/v1/admin/dashboard/` |
| **Usuarios** | GET, POST | `/api/v1/admin/users/` |
| **Usuario (detalle)** | GET, PUT, DELETE | `/api/v1/admin/users/{id}/` |
| **Órdenes (todas)** | GET | `/api/v1/admin/all-orders/` |
| **Orden (detalle)** | GET, PATCH, DELETE | `/api/v1/admin/all-orders/{id}/` |
| **Actualizar estado orden** | POST | `/api/v1/admin/all-orders/{id}/update_status/` |
| **Productos** | GET, POST | `/api/v1/admin/products/` |
| **Producto (detalle)** | GET, PUT, DELETE | `/api/v1/admin/products/{id}/` |
| **Productos destacados** | GET | `/api/v1/admin/products/featured/` |
| **Categorías** | GET, POST | `/api/v1/admin/categories/` |
| **Categoría (detalle)** | GET, PUT, DELETE | `/api/v1/admin/categories/{id}/` |
| **Subcategorías** | GET | `/api/v1/admin/categories/{id}/subcategories/` |
| **Imágenes** | GET, POST, DELETE | `/api/v1/admin/product-images/` |

---

## 1. Dashboard

**¿Qué puede hacer el usuario?**
- Ver estadísticas generales del negocio
- Ver cuántas órdenes hay en cada estado
- Ver ingresos totales

### GET /api/v1/admin/dashboard/
Estadísticas completas del sistema.

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

**¿Qué puede hacer el usuario?**
- Ver lista de todos los usuarios registrados
- Crear nuevos usuarios (clientes o administradores)
- Editar datos de usuarios existentes
- Activar/desactivar usuarios
- Eliminar usuarios
- Hacer usuarios administradores (is_staff)

### Listar usuarios
```
GET /api/v1/admin/users/
```
**Query params:** `?search=email&ordering=-created_at&page=1`

**Response:**
```json
{
    "count": 25,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "email": "admin@admin.com",
            "username": "admin",
            "first_name": "Admin",
            "last_name": "User",
            "phone": "+5351234567",
            "address": "",
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
```
**Request:**
```json
{
    "email": "usuario@email.com",
    "username": "usuario",
    "password": "password123",
    "password_confirm": "password123",
    "first_name": "Juan",
    "last_name": "Pérez",
    "phone": "+5351234567",
    "is_staff": false,
    "is_active": true
}
```

### Actualizar usuario
```
PUT /api/v1/admin/users/{id}/
```
**Request (parcial):**
```json
{
    "first_name": "Nuevo nombre",
    "is_active": false,
    "is_staff": true
}
```

### Eliminar usuario
```
DELETE /api/v1/admin/users/{id}/
```

---

## 3. Órdenes (todas)

**¿Qué puede hacer el usuario?**
- Ver todas las órdenes del sistema (no solo las propias)
- Ver detalle de cada orden (productos, cliente, dirección)
- Cambiar estado de la orden (pending → processing → completed/cancelled)
- Eliminar órdenes
- Buscar órdenes por cliente, teléfono

### Listar todas las órdenes
```
GET /api/v1/admin/all-orders/
```
**Query params:** `?status=pending&search=juan&ordering=-created_at&page=1`

**Response:**
```json
{
    "count": 100,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "user": 1,
            "products": [
                {
                    "id": 1,
                    "name": "iPhone 15 Pro",
                    "price": "999.99",
                    "quantity": 2,
                    "subtotal": "1999.98"
                }
            ],
            "total_amount": "1999.98",
            "status": "pending",
            "customer_name": "Juan Pérez",
            "customer_phone": "+5351234567",
            "customer_address": "Calle 123, La Habana",
            "notes": "Llamar al llegar",
            "created_at": "2024-01-01T00:00:00Z",
            "updated_at": "2024-01-01T00:00:00Z"
        }
    ]
}
```

**Estados posibles:** `pending`, `processing`, `completed`, `cancelled`

### Ver orden específica
```
GET /api/v1/admin/all-orders/{id}/
```

### Actualizar estado de orden
```
POST /api/v1/admin/all-orders/{id}/update_status/
```
**Request:**
```json
{
    "status": "completed"
}
```

**Estados válidos:** `pending`, `processing`, `completed`, `cancelled`

### Eliminar orden
```
DELETE /api/v1/admin/all-orders/{id}/
```

---

## 4. Productos

**¿Qué puede hacer el usuario?**
- Ver lista de todos los productos
- Crear nuevos productos (nombre, precio, stock, categoría)
- Editar productos (precio, descripción, stock, categoría)
- Activar/desactivar productos (ocultar sin borrar)
- Eliminar productos
- Agregar imágenes a productos
- Buscar productos por nombre
- Filtrar por categoría

### Listar productos
```
GET /api/v1/admin/products/
```
**Query params:** `?search=iphone&category=1&ordering=-created_at&page=1`

**Response:**
```json
{
    "count": 40,
    "next": "http://.../admin/products/?page=2",
    "previous": null,
    "results": [
        {
            "id": 40,
            "name": "Revista Tech",
            "slug": "revista-tech",
            "description": "High quality Revista Tech...",
            "price": "5.99",
            "compare_price": null,
            "stock": 100,
            "category": {
                "id": 25,
                "name": "Revistas",
                "slug": "revistas"
            },
            "main_image": {
                "id": 14,
                "image": "/api/v1/media/products/product_40_1.jpg",
                "alt_text": "Revista Tech - Imagen 1",
                "is_primary": true
            },
            "is_active": true,
            "created_at": "2026-02-21T16:44:48.059808-05:00"
        }
    ]
}
```

### Crear producto
```
POST /api/v1/admin/products/
```
**Request:**
```json
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

**Campos:**
- `name` (requerido): Nombre del producto
- `description`: Descripción
- `price` (requerido): Precio
- `compare_price`: Precio anterior (para mostrar descuento)
- `stock`: Cantidad en inventario
- `category` (requerido): ID de categoría
- `subcategory`: ID de subcategoría (opcional)
- `is_active`: Boolean - si el producto está visible
- `image_ids`: Array de IDs de imágenes

### Actualizar producto
```
PUT /api/v1/admin/products/{id}/
```
**Request (ejemplo):**
```json
{
    "name": "Producto Actualizado",
    "price": 79.99,
    "stock": 5,
    "is_active": true,
    "image_ids": [1, 4, 5]
}
```

### Eliminar producto
```
DELETE /api/v1/admin/products/{id}/
```

### Productos destacados
```
GET /api/v1/admin/products/featured/
```
Retorna hasta 10 productos con stock > 0.

---

## 5. Categorías

**¿Qué puede hacer el usuario?**
- Ver lista de categorías y subcategorías
- Crear nuevas categorías (raíz o subcategorías)
- Editar categorías (nombre, descripción)
- Activar/desactivar categorías
- Eliminar categorías
- Ver subcategorías de una categoría
- Ver cantidad de productos en cada categoría

### Listar categorías
```
GET /api/v1/admin/categories/
```
**Query params:** `?search=electronica&ordering=name`

**Response:**
```json
[
    {
        "id": 1,
        "name": "Electronica",
        "slug": "electronica",
        "description": "Devices and electronics",
        "image": "/api/v1/media/categories/electronica.jpg",
        "parent": null,
        "subcategories": [
            {"id": 2, "name": "Smartphones", "slug": "smartphones"},
            {"id": 3, "name": "Laptops", "slug": "laptops"}
        ],
        "products_count": 50,
        "is_active": true,
        "created_at": "2024-01-01T00:00:00Z"
    }
]
```

### Crear categoría
```
POST /api/v1/admin/categories/
```
**Request:**
```json
{
    "name": "Nueva Categoría",
    "description": "Descripción",
    "parent": null,
    "is_active": true
}
```

- `parent`: ID de categoría padre (null = categoría raíz)

### Actualizar categoría
```
PUT /api/v1/admin/categories/{id}/
```
**Request:**
```json
{
    "name": "Categoría Actualizada",
    "is_active": false
}
```

### Eliminar categoría
```
DELETE /api/v1/admin/categories/{id}/
```

### Subcategorías
```
GET /api/v1/admin/categories/{id}/subcategories/
```

---

## 6. Imágenes

**¿Qué puede hacer el usuario?**
- Subir nuevas imágenes al sistema
- Ver todas las imágenes subidas
- Eliminar imágenes
- Usar el ID de la imagen al crear/editar productos

### Subir imagen
```
POST /api/v1/admin/product-images/
Content-Type: multipart/form-data
```
**Body:** `image=archivo.jpg`

**Response:**
```json
{
    "id": 1,
    "image": "/api/v1/media/products/nuevo.jpg",
    "alt_text": "",
    "is_primary": false,
    "created_at": "2024-01-01T00:00:00Z"
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

**Response:**
```json
{
    "user": {
        "id": 1,
        "email": "admin@admin.com",
        "is_staff": true,
        "is_superuser": true,
        ...
    },
    "tokens": {
        "refresh": "eyJ...",
        "access": "eyJ..."
    }
}
```

---

## Cómo saber si es admin

En el login o perfil, verificar:
- `user.is_staff === true` → Acceso admin
- `user.is_superuser === true` → Super usuario

```javascript
const { user } = await loginResponse.json();
if (user.is_staff || user.is_superuser) {
    // Mostrar panel de admin
}
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

// ======================
// DASHBOARD
// ======================
const dash = await fetch(`${API}/admin/dashboard/`, { headers });
const stats = await dash.json();
// stats.orders.total, stats.orders.pending, etc.

// ======================
// PRODUCTOS
// ======================
// Listar
const products = await fetch(`${API}/admin/products/`, { headers });
const productsData = await products.json();

// Crear
await fetch(`${API}/admin/products/`, {
    method: 'POST',
    headers,
    body: JSON.stringify({
        name: 'Nuevo Producto',
        price: 99.99,
        stock: 10,
        category: 1,
        is_active: true
    })
});

// ======================
// ÓRDENES
// ======================
// Listar todas
const orders = await fetch(`${API}/admin/all-orders/`, { headers });
const ordersData = await orders.json();

// Cambiar estado
await fetch(`${API}/admin/all-orders/1/update_status/`, {
    method: 'POST',
    headers,
    body: JSON.stringify({ status: 'completed' })
});

// ======================
// CATEGORÍAS
// ======================
const categories = await fetch(`${API}/admin/categories/`, { headers });

// ======================
// IMÁGENES
// ======================
// Subir
const formData = new FormData();
formData.append('image', fileInput.files[0]);
await fetch(`${API}/admin/product-images/`, {
    method: 'POST',
    headers: { 'Authorization': `Bearer ${token}` },
    body: formData
});
```

---

## Notas Importantes

1. **Paginación**: Todos los endpoints de lista usan paginación (`?page=2`)
2. **Búsqueda**: Usar `?search=termino` 
3. **Ordenamiento**: `?ordering=-created_at` (negativo = descendente)
4. **Filtros**: `?status=pending&category=1`
5. **Imágenes**: Las imágenes se servent desde `/api/v1/media/...`
6. **Productos**: El campo `category` es un objeto con `id`, `name`, `slug`
7. **Fechas**: Usan formato ISO con timezone (`2026-02-21T16:44:48-05:00`)
