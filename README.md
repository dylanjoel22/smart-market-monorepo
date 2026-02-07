# Smart Market - Comparador de Precios Inteligente

Sistema de Business Intelligence para retail orientado al monitoreo de precios en supermercados chilenos. Detecta ahorros reales mediante la comparación dinámica de precios de lista vs. ofertas en tiempo de ingesta, con soporte especializado para **Precios Club**.

---

## Características Técnicas

- **Scraping Masivo:** Crawling automático de **14 categorías** de productos con paginación adaptativa.
- **Historial Multicentro:** Registro de precios por fecha, sucursal y región (Antofagasta y Tocopilla actualmente operativos).
- **Gestión de Precio Club:** Captura y limpieza de precios especiales asociados a métodos de pago específicos.
- **Validación de Ofertas:** Algoritmo interno que determina la veracidad de una oferta sin depender de los flags de la API de origen.
- **Deduplicación por EAN:** Uso del código de barras como ancla universal para evitar duplicados en el catálogo.
- **Rate Limiting:** Implementación de delays aleatorios (**1-3s**) para garantizar una extracción ética y evitar bloqueos.

---

## Stack

- **Backend:** Django 6.0.1 + Django REST Framework 3.16.1.
- **Frontend:** Vite + React (En desarrollo).
- **Base de Datos:** PostgreSQL.
- **Extracción de Datos:** Requests y BeautifulSoup4.
- **Seguridad:** `python-dotenv` para gestión de secretos.

---

## Arquitectura de Datos

El sistema utiliza una estructura relacional diseñada para la escalabilidad geográfica y temporal:

- **Market:** Entidad global que representa la cadena de retail (ej. Unimarc).
- **Branch:** Sucursal específica vinculada a un ID de zona para la API (ej. Tocopilla ID: 59, Antofagasta ID: 55).
- **Product:** Catálogo único de productos donde el EAN actúa como clave primaria lógica para la deduplicación.
- **PriceSnapshot:** Registro histórico de precios vinculado a un producto, una sucursal y una marca temporal de extracción.

---
