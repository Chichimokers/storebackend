# Documentación API - Tienda Online

## Base URL

```
https://inventory.cloduns.be/api/v1/
```

---

## 1. Autenticación

### Registro de usuario

```
POST /users/register/
Content-Type: application/json

Request:
{
    "email": "usuario@email.com",
    "username": "usuario123",
    "password": "password123",
    "password_confirm": "password123",
    "first_name": "Juan",
    "last_name": "Pérez",
    "phone": "+5351234567"
}

Response (201):
{
    "user": {
        "id": 1,
        "email": "usuario@email.com",
        "username": "usuario123",
        "first_name": "Juan",
        "last_name": "Pérez",
        "phone": "+5351234567",
        "address": "",
        "created_at": "2024-01-01T00:00:00Z"
    },
    "tokens": {
        "refresh": "eyJ...",
        "access": "eyJ..."
    }
}
```

### Login

```
POST /users/login/
Content-Type: application/json

Request:
{
    "email": "usuario@email.com",
    "password": "password123"
}

Response (200):
{
    "user": {...},
    "tokens": {
        "refresh": "eyJ...",
        "access": "eyJ..."
    }
}
```

### Refresh Token

```
POST /users/token/refresh/
Content-Type: application/json

Request:
{
    "refresh": "eyJ..."
}

Response (200):
{
    "access": "eyJ..."
}
```

### Perfil del usuario

```
GET /users/profile/
Authorization: Bearer <token>

Response (200):
{
    "id": 1,
    "email": "usuario@email.com",
    "username": "usuario123",
    "first_name": "Juan",
    "last_name": "Pérez",
    "phone": "+5351234567",
    "address": "Calle 123, La Habana",
    "created_at": "2024-01-01T00:00:00Z"
}
```

### Actualizar perfil

```
PUT /users/profile/
Authorization: Bearer <token>
Content-Type: application/json

Request:
{
    "first_name": "Juan",
    "last_name": "Pérez",
    "phone": "+5351234567",
    "address": "Calle 123, La Habana"
}

Response (200): {...}
```

---

## 2. Productos

### Listar productos

```
GET /products/
Query Params (opcionales):
    - category: ID de categoría
    - subcategory: ID de subcategoría
    - search: Buscar por nombre
    - ordering: price, -price, name, created_at
    - page: Número de página

Response (200):
{
    "count": 100,
    "next": "https://.../api/v1/products/?page=2",
    "previous": null,
    "results": [
        {
            "id": 1,
            "name": "iPhone 15 Pro",
            "slug": "iphone-15-pro",
            "description": "...",
            "price": "999.99",
            "compare_price": "1099.99",
            "stock": 10,
            "category": {
                "id": 1,
                "name": "Electrónica",
                "slug": "electronica"
            },
            "main_image": {
                "id": 1,
                "image": "/api/v1/media/products/iphone.jpg",
                "is_primary": true
            },
            "is_active": true,
            "created_at": "2024-01-01T00:00:00Z"
        }
    ]
}
```

### Detalle de producto

```
GET /products/{id}/
Response (200):
{
    "id": 1,
    "name": "iPhone 15 Pro",
    "slug": "iphone-15-pro",
    "description": "Descripción completa del producto...",
    "price": "999.99",
    "compare_price": "1099.99",
    "stock": 10,
    "category": {...},
    "subcategory": null,
    "images": [
        {"id": 1, "image": "/api/v1/media/products/img1.jpg", "is_primary": true},
        {"id": 2, "image": "/api/v1/media/products/img2.jpg", "is_primary": false}
    ],
    "is_active": true,
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z"
}
```

### Productos destacados

```
GET /products/featured/
Response (200): [...] // Lista de productos
```

---

## 3. Categorías

### Listar categorías (raíz)

```
GET /products/categories/
Response (200):
[
    {
        "id": 1,
        "name": "Electrónica",
        "slug": "electronica",
        "description": "...",
        "image": "/api/v1/media/categories/electronica.jpg",
        "parent": null,
        "subcategories": [
            {"id": 2, "name": "Smartphones", "slug": "smartphones"},
            {"id": 3, "name": "Laptops", "slug": "laptops"}
        ],
        "products_count": 50,
        "is_active": true
    }
]
```

### Subcategorías de una categoría

```
GET /products/categories/{id}/subcategories/
Response (200):
[
    {"id": 2, "name": "Smartphones", "slug": "smartphones"},
    {"id": 3, "name": "Laptops", "slug": "laptops"}
]
```

---

## 4. Órdenes

### Checkout - Generar orden y mensaje WhatsApp

**IMPORTANTE:** Este endpoint requiere autenticación. El usuario debe estar logueado.

```
POST /orders/checkout/
Authorization: Bearer <token>
Content-Type: application/json

Request:
{
    "products": [
        {"id": 1, "quantity": 2},
        {"id": 5, "quantity": 1}
    ],
    "customer_name": "Juan Pérez",
    "customer_phone": "+5351234567",
    "customer_address": "Calle 123, La Habana",
    "notes": "Entregar en la tarde"
}

Response (200):
{
    "order_id": 1,
    "phone": "+1234567890",
    "message": "Hola, mi nombre es Juan Pérez. Quiero comprar:\n\n- iPhone 15 Pro x2 = $1999.98\n- AirPods Pro x1 = $249.99\n\nTotal: $2249.97",
    "whatsapp_url": "https://wa.me/1234567890?text=Hola%2C%20mi%20nombre%20es%20Juan%20P%C3%A9rez...",
    "order_total": "2249.97"
}
```

**Notas:**
- La orden se guarda en la base de datos asociada al usuario autenticado
- El mensaje de WhatsApp va al número de la tienda configurado en `WHATSAPP_PHONE`
- El usuario es redirigido al link de WhatsApp para completar la compra

### Mis órdenes

```
GET /orders/
Authorization: Bearer <token>

Response (200):
{
    "count": 5,
    "results": [
        {
            "id": 1,
            "products": [...],
            "total_amount": "1999.98",
            "status": "pending",
            "customer_name": "Juan Pérez",
            "created_at": "2024-01-01T00:00:00Z"
        }
    ]
}
```

### Ver orden específica

```
GET /orders/{id}/
Authorization: Bearer <token>
```

---

## 5. Imágenes de productos

### Subir imagen

```
POST /products/images/
Authorization: Bearer <token> (admin)
Content-Type: multipart/form-data

Request:
- image: archivo de imagen

Response (201):
{
    "id": 1,
    "image": "/api/v1/media/products/image.jpg",
    "alt_text": "",
    "is_primary": false
}
```

---

# Guía para el Frontend

## Estructura de la Tienda

### 1. Header/Navegación

- Logo de la tienda
- Menú de categorías (carga desde `/products/categories/`)
- Icono de carrito
- Botones: Login / Mi Cuenta / Cerrar Sesión

### 2. Página Principal (Home)

- **Banner principal**: Imagen grande promocional
- **Categorías destacadas**: Grid de categorías con imagen
- **Productos destacados**: Slider o grid desde `/products/featured/`
- **Productos recientes**: Desde `/products/` (ordering=-created_at)

### 3. Catálogo de Productos

- **Sidebar/Filtros**:
  - Categorías (carga `/products/categories/`)
  - Subcategorías (al hacer click en categoría)
  - Rango de precio
  - Buscador (parámetro `search`)
- **Grid de productos**: Desde `/products/?category=X`
- **Paginación**: Incluye en la respuesta

### 4. Detalle de Producto

- **Galería de imágenes**: `/products/{id}/` → campo `images`
- **Información**:
  - Nombre, descripción
  - Precio (mostrar `compare_price` tachado si existe)
  - Stock disponible
  - Categoría / Subcategoría
- **Cantidad**: Input numérico (min 1, max = stock)
- **Botón "Agregar al carrito"**
- **Botón "Comprar ahora"** → направляет a checkout

### 5. Carrito de Compras

- **Estado**: LocalStorage o contexto global
- **Estructura**:
  ```json
  [{ "id": 1, "name": "Producto", "price": 100, "quantity": 2, "image": "..." }]
  ```
- **Funciones**:
  - Cambiar cantidad
  - Eliminar producto
  - Calcular total
  - Vaciar carrito

### 6. Checkout (Página crítica)

**IMPORTANTE:** El usuario debe estar autenticado para hacer checkout.

**Flujo de compra:**

```
1. Carrito → Botón "Proceder al pago"
2. Verificar que usuario está logueado (si no, redirigir a login)
3. Mostrar resumen del carrito
4. Formulario del cliente (datos del perfil):
   - Nombre completo (del perfil)
   - Teléfono *
   - Dirección de entrega
   - Notas adicionales
5. Botón "Finalizar compra"
```

**Al hacer click en "Finalizar compra":**

```javascript
// Verificar que hay token de autenticación
const token = localStorage.getItem('access_token');
if (!token) {
    // Redirigir a login
    window.location.href = '/login/?next=/checkout/';
    return;
}

// Llamar al endpoint checkout (requiere autenticación)
const response = await fetch('/api/v1/orders/checkout/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify({
        products: [
            {id: 1, quantity: 2},
            {id: 5, quantity: 1}
        ],
        customer_name: "Juan Pérez",
        customer_phone: "+5351234567",
        customer_address: "Calle 123",
        notes: "Entregar en la tarde"
    })
});

const data = await response.json();

// El backend retorna:
{
    "order_id": 1,
    "whatsapp_url": "https://wa.me/1234567890?text=..."
}

// Guardar ID de orden para referencia
localStorage.setItem('last_order_id', data.order_id);

// Redirect a WhatsApp
window.open(data.whatsapp_url, '_blank');

// Opcional: vaciar carrito
localStorage.removeItem('cart');
```

**Nota:** El mensaje de WhatsApp va al número de la tienda (`WHATSAPP_PHONE`), no al cliente.

### 7. Mi Cuenta (Dashboard)

- **Información personal**: GET `/users/profile/`
- **Editar perfil**: PUT `/users/profile/`
- **Historial de pedidos**: GET `/orders/`
- **Cerrar sesión**

---

## Modelos de Datos en Frontend

### Producto

```typescript
interface Product {
  id: number;
  name: string;
  slug: string;
  description: string;
  price: number;
  compare_price: number | null;
  stock: number;
  category: Category;
  subcategory: Category | null;
  images: ProductImage[];
  main_image: ProductImage | null;
}

interface ProductImage {
  id: number;
  image: string;
  is_primary: boolean;
}

interface Category {
  id: number;
  name: string;
  slug: string;
  image: string | null;
  subcategories: Category[];
  products_count: number;
}
```

### Carrito

```typescript
interface CartItem {
  id: number; // ID del producto
  name: string;
  price: number;
  quantity: number;
  image: string | null;
  maxStock: number;
}

interface Cart {
  items: CartItem[];
  total: number;
}
```

### Orden

```typescript
interface Order {
  id: number;
  products: OrderProduct[];
  total_amount: number;
  status: "pending" | "processing" | "completed" | "cancelled";
  customer_name: string;
  customer_phone: string;
  customer_address: string;
  notes: string;
  created_at: string;
}

interface OrderProduct {
  id: number;
  name: string;
  price: string;
  quantity: number;
  subtotal: string;
}
```

---

## Páginas Requeridas

| Página           | Descripción                    | Endpoint principal      |
| ---------------- | ------------------------------ | ----------------------- |
| Home             | Portada con promociones        | `/products/featured/`   |
| Catálogo         | Lista de productos con filtros | `/products/`            |
| Categoría        | Productos por categoría        | `/products/?category=X` |
| Producto Detalle | Info completa del producto     | `/products/{id}/`       |
| Carrito          | Ver/edit items                 | LocalStorage            |
| Checkout         | Formulario + WhatsApp          | `/orders/checkout/`     |
| Login            | Iniciar sesión                 | `/users/login/`         |
| Registro         | Crear cuenta                   | `/users/register/`      |
| Mi Perfil        | Datos del usuario              | `/users/profile/`       |
| Mis Pedidos      | Historial                      | `/orders/`              |
| Admin            | Panel administración           | `/api/v1/admin/`        |

---

## Notas Importantes

1. **Imágenes**: Vienen en formato `/api/v1/media/...`. Concatenar con el dominio.

2. **Autenticación**:
   - Guardar `access` token en localStorage/sessionStorage
   - Incluir en headers: `Authorization: Bearer <token>`
   - Si el token expira, usar `/users/token/refresh/` con el `refresh` token

3. **Precios**: Vienen como strings (ej: "999.99"). Convertir a número para cálculos.

4. **WhatsApp**: El flujo es:
   - Frontend genera el pedido
   - Backend genera URL de WhatsApp
   - Usuario es redirigido a WhatsApp
   - El admin recibe el mensaje y procesa la orden manualmente

5. **Stock**: Verificar siempre el stock antes de permitir agregar al carrito.

6. **Categorías con jerarquía**:
   - Las categorías principales tienen `parent: null`
   - Las subcategorías tienen `parent: ID`
   - Usar `/categories/{id}/subcategories/` para obtener subcategorías

---

## Ejemplo: Flujo Completo de Compra

```javascript
// 1. Usuario ve productos
const products = await fetch("/api/v1/products/").then((r) => r.json());

// 2. Usuario selecciona producto
const product = await fetch("/api/v1/products/1/").then((r) => r.json());

// 3. Usuario agrega al carrito (localStorage)
let cart = JSON.parse(localStorage.getItem("cart") || "[]");
cart.push({
  id: product.id,
  name: product.name,
  price: product.price,
  quantity: 1,
  image: product.main_image?.image,
});
localStorage.setItem("cart", JSON.stringify(cart));

// 4. Usuario va a checkout
// Verificar que está autenticado
const token = localStorage.getItem('access_token');
if (!token) {
    // Redirigir a login con retorno a checkout
    window.location.href = '/login/?next=/checkout/';
}

// 5. Usuario completa formulario (o usa datos del perfil)
const checkoutData = {
    products: cart.map(item => ({id: item.id, quantity: item.quantity})),
    customer_name: "Juan Pérez",
    customer_phone: "+5351234567",
    customer_address: "Calle 123, La Habana",
    notes: "Entregar en la tarde"
};

// 6. Llamar checkout (con autenticación)
const result = await fetch("/api/v1/orders/checkout/", {
    method: "POST",
    headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`
    },
    body: JSON.stringify(checkoutData),
}).then(r => r.json());

// 7. La orden ya está guardada en BD (order_id)
// El backend retorna el link de WhatsApp
// {
//     "order_id": 1,
//     "whatsapp_url": "https://wa.me/1234567890?text=..."
// }

// 8. Redirigir a WhatsApp para completar la compra
window.open(result.whatsapp_url, "_blank");

// 9. Vaciar carrito
localStorage.removeItem('cart');

// 10. Opcional: Ver en "Mis órdenes"
const orders = await fetch("/api/v1/orders/", {
    headers: {"Authorization": `Bearer ${token}`}
}).then(r => r.json());
    ...checkoutData,
    customer_address: "Dirección...",
    notes: "Notas...",
  }),
});
```
