# 📸 Scrapy Datos Instagram

<div align="center">

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge\&logo=python\&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge\&logo=flask\&logoColor=white)
![Playwright](https://img.shields.io/badge/Playwright-2EAD33?style=for-the-badge\&logo=playwright\&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge\&logo=pandas\&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge\&logo=html5\&logoColor=white)
![Instagram](https://img.shields.io/badge/Instagram-E4405F?style=for-the-badge\&logo=instagram\&logoColor=white)

<h3>🔥 Sistema de Scraping de Instagram con Flask + Playwright 🔥</h3>

<p>
Obtiene información pública de perfiles de Instagram, incluyendo seguidores, publicaciones,
likes, comentarios y exportación de datos a Excel.
</p>

</div>

---

# ✨ Características

✅ Scraping automático de perfiles de Instagram
✅ Obtención de seguidores y publicaciones
✅ Extracción de las primeras 10 publicaciones
✅ Conteo de likes y comentarios
✅ Visualización de imágenes de publicaciones
✅ API REST con Flask
✅ Exportación de datos a Excel (.xlsx)
✅ Frontend simple y dinámico
✅ Uso de sesión real de Chrome

---

# 🖼️ Vista General del Proyecto

```text
Usuario -> Frontend Flask -> API -> Playwright -> Instagram
                                    ↓
                           Procesamiento de datos
                                    ↓
                              Exportación Excel
```

---

# 🛠️ Tecnologías Utilizadas

<div align="center">

<img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg" width="80" height="80" alt="Python" />
<img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/flask/flask-original.svg" width="80" height="80" alt="Flask" />
<img src="https://playwright.dev/img/playwright-logo.svg" width="80" height="80" alt="Playwright" />
<img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/pandas/pandas-original.svg" width="80" height="80" alt="Pandas" />
<img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/html5/html5-original.svg" width="80" height="80" alt="HTML5" />
<img src="https://upload.wikimedia.org/wikipedia/commons/a/a5/Instagram_icon.png" width="80" height="80" alt="Instagram" />

</div>

---

---

# 📂 Estructura del Proyecto

```bash
Scrapy_datos/
│
├── scrapingIG.py          # Backend principal
├── templates/
│   └── index.html         # Frontend
├── userdata/              # Sesión persistente de Chrome
└── README.md
```

---

# ⚙️ Instalación

## 1️⃣ Clonar el repositorio

```bash
git clone https://github.com/TU-USUARIO/Scrapy_datos.git
```

---

## 2️⃣ Entrar al proyecto

```bash
cd Scrapy_datos
```

---

## 3️⃣ Crear entorno virtual

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / Mac

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 4️⃣ Instalar dependencias

```bash
pip install flask playwright pandas openpyxl
```

---

## 5️⃣ Instalar navegadores de Playwright

```bash
playwright install
```

---

# ▶️ Ejecutar el Proyecto

```bash
python scrapingIG.py
```

El servidor iniciará en:

```bash
http://127.0.0.1:5000
```

---

# 🔥 Endpoints de la API

## 📌 Obtener información de un perfil

```http
GET /api/scrape/<username>
```

### Ejemplo

```http
GET /api/scrape/cristiano
```

### Respuesta

```json
{
  "status": "success",
  "data": {
    "usuario": "cristiano",
    "seguidores": "651M",
    "publicaciones": "3900",
    "posts": [
      {
        "post": 1,
        "likes": "2.5M",
        "comentarios": "35K",
        "imagen": "url"
      }
    ]
  }
}
```

---

## 📥 Exportar datos a Excel

```http
GET /api/export/<username>
```

### Ejemplo

```http
GET /api/export/cristiano
```

---

# 🧠 Funcionamiento del Sistema

El sistema realiza los siguientes pasos:

1. Abre una sesión persistente de Chrome.
2. Accede al perfil de Instagram.
3. Extrae seguidores y publicaciones.
4. Analiza las publicaciones.
5. Obtiene likes y comentarios.
6. Devuelve los datos mediante una API REST.
7. Permite exportar la información a Excel.

---

# 🔐 Nota Importante

⚠️ Instagram puede solicitar inicio de sesión para acceder correctamente a algunos perfiles.

Por ello, el proyecto utiliza:

```python
launch_persistent_context()
```

Esto permite mantener una sesión real de Chrome guardada en:

```bash
userdata/
```

---

# 📊 Librerías Principales

## 🎭 Playwright

Utilizado para:

* Automatización del navegador
* Interacción con Instagram
* Obtención dinámica de datos
* Simulación de usuario real

---

## 🌐 Flask

Utilizado para:

* Crear API REST
* Renderizar frontend
* Exportar archivos
* Comunicación cliente-servidor

---

## 📈 Pandas

Utilizado para:

* Manipular datos
* Crear tablas
* Exportar archivos Excel

---

# 🧠 Lógica Utilizada en el Proyecto

El proyecto sigue una arquitectura basada en automatización web + API REST.

## 🔄 Flujo General del Sistema

```text
Usuario ingresa un username
            ↓
Flask recibe la solicitud
            ↓
Playwright abre Instagram
            ↓
Se realiza el scraping del perfil
            ↓
Se extraen publicaciones, likes y comentarios
            ↓
Los datos se procesan con Python y Pandas
            ↓
Flask devuelve la información al frontend o exporta a Excel
```

---

## ⚙️ Lógica Implementada

### 1️⃣ Automatización del Navegador

Se utiliza Playwright para controlar un navegador Chromium real.

El navegador:

* Accede automáticamente al perfil de Instagram.
* Espera que el contenido cargue dinámicamente.
* Busca los elementos HTML necesarios.
* Extrae información pública del perfil.

---

### 2️⃣ Uso de Sesión Persistente

Instagram posee mecanismos anti-bots.

Para evitar bloqueos constantes, el sistema utiliza:

```python
launch_persistent_context()
```

Esto permite:

✅ Mantener cookies
✅ Conservar sesiones iniciadas
✅ Simular un navegador real
✅ Reducir restricciones de Instagram

---

### 3️⃣ Extracción de Publicaciones

La lógica del scraping:

* Obtiene las primeras publicaciones del perfil.
* Ingresa individualmente a cada publicación.
* Extrae:

  * likes
  * comentarios
  * imagen
  * enlace

Esto permite analizar el rendimiento del contenido del perfil.

---

### 4️⃣ Procesamiento de Datos

Los datos extraídos se almacenan temporalmente en estructuras de Python.

Posteriormente Pandas:

* organiza la información,
* crea tablas,
* y exporta archivos Excel.

---

### 5️⃣ API REST con Flask

Flask actúa como intermediario entre:

* el frontend,
* el scraper,
* y la exportación de datos.

La API permite:

✅ Consultar perfiles
✅ Obtener publicaciones
✅ Descargar archivos Excel

---

# ⚠️ Desafíos Encontrados Durante el Desarrollo

## 🚫 Restricciones de Instagram

Uno de los principales problemas fue que Instagram detecta automatizaciones fácilmente.

### Problemas encontrados:

* Bloqueos temporales
* Solicitud de login
* Captchas
* Contenido que no cargaba
* Límites de peticiones

### Solución aplicada:

✅ Uso de sesión persistente
✅ Simulación de comportamiento humano
✅ Esperas dinámicas con Playwright

---

## ⏳ Carga Dinámica del Contenido

Instagram carga muchos elementos mediante JavaScript.

Esto provocaba:

* elementos inexistentes al inicio,
* errores de scraping,
* y tiempos inconsistentes.

### Solución:

Se utilizaron:

```python
wait_for_selector()
```

y tiempos de espera controlados para garantizar que los elementos estuvieran completamente cargados.

---

## 🧩 Cambios Constantes en el HTML de Instagram

Instagram modifica frecuentemente:

* clases CSS,
* estructuras HTML,
* selectores.

Esto afecta directamente al scraping.

### Solución:

Se utilizaron selectores más flexibles y estrategias de búsqueda menos dependientes de clases estáticas.

---

## 📊 Exportación Correcta de Datos

Otro desafío fue estructurar correctamente la información obtenida.

### Problemas:

* Datos incompletos
* Valores nulos
* Formatos inconsistentes

### Solución:

Se procesaron los datos con Pandas antes de exportarlos a Excel.

---

## 🌐 Comunicación Frontend ↔ Backend

Se necesitó coordinar correctamente:

* solicitudes HTTP,
* respuestas JSON,
* renderizado de publicaciones,
* y descarga de archivos.

### Resultado:

Se logró una integración funcional entre Flask y el frontend.

---

# 🚀 Posibles Mejoras Futuras

✅ Login automático
✅ Dashboard avanzado
✅ Base de datos
✅ Exportación CSV y PDF
✅ Scraping masivo
✅ Gráficas estadísticas
✅ Sistema de autenticación
✅ Dockerización
✅ Deploy en Render o Railway

---

# 👨‍💻 Autor

<div align="center">

## ✨ Desarrollado por María de los Ángeles Taco ✨

Proyecto desarrollado con Python, Flask y Playwright.

</div>

---

# ⭐ Apoya el Proyecto

Si te gustó este proyecto:

🌟 Dale una estrella en GitHub
🍴 Haz un fork del repositorio
📢 Compártelo con otros desarrolladores

---

# 📜 Licencia

Este proyecto es únicamente con fines educativos y de aprendizaje.

El uso del scraping debe respetar los términos y condiciones de Instagram.
