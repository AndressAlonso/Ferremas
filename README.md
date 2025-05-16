# 🛠️ FERREMAS - Plataforma de Comercio Electrónico

**Proyecto Final de la Asignatura:** Integración de Plataformas (ASY5131)  
**Institución:** Subdirección de Evaluación de Resultados de Aprendizaje  
**Caso de Estudio:** Distribuidora FERREMAS  
**Lenguaje:** Python + Django  
**Base de Datos:** MySQL / SQLite (según configuración local)  
**Tipo de entrega:** Encargo con presentación (Evaluación Final Transversal)

---

## 📌 Descripción General

Este proyecto consiste en el desarrollo de una solución tecnológica para la empresa chilena **FERREMAS**, una distribuidora de productos de ferretería y construcción con operaciones presenciales y necesidades de transformación digital.

El sistema busca digitalizar sus operaciones a través de una **plataforma e-commerce** robusta, con integración de roles organizacionales, gestión de pedidos, API/WebService, y funcionalidades de venta en línea.

---

## 🎯 Objetivos

- Mejorar la eficiencia operativa y la experiencia de compra.
- Integrar un modelo de negocio físico con operaciones en línea.
- Permitir gestión por roles: administrador, vendedor, bodeguero, contador y cliente.
- Implementar WebServices/API REST para integración interna y externa.
- Validar el sistema con pruebas unitarias, de integración y documentación técnica.

---

## 🧩 Funcionalidades Principales

### 👤 Autenticación y Roles

- Login con validación por tipo de usuario (admin, cliente, vendedor, etc.).
- Clientes se registran libremente.
- Otros roles son creados por el administrador.

### 🛒 Clientes

- Visualización de productos y detalles.
- Carrito de compras y creación de pedidos.
- Selección de tipo de entrega (retiro o despacho).
- Métodos de pago: débito, crédito, transferencia.
- Historial de compras.

### 🧑‍💼 Vendedores

- Visualización de pedidos nuevos.
- Aprobación o rechazo de pedidos.
- Envío a bodega para preparación.

### 📦 Bodegueros

- Visualización de pedidos listos para despacho.
- Preparación y marcado como entregado.
- Generación automática de ventas finalizadas.

### 🧮 Contadores

- Confirmación de pagos por transferencia.
- Registro de pagos y validación.

### 🧠 Administradores

- Reportes de venta y desempeño.
- Gestión de usuarios y control del sistema.

---

## 🌐 API / WebService

El sistema incluye una **API RESTful** que permite:

- Consultar productos con stock, marcas, modelos, códigos y precios.
- Uso interno por sucursales.
- Integración externa para otras tiendas y sistemas.

---
