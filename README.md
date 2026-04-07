# 📥 Instagram Video Downloader con Docker

Aplicación web desarrollada con **Python + Flask** y **yt-dlp** para descargar videos de redes sociales (Instagram, YouTube, TikTok, Facebook, LinkedIn). Containerizada con Docker aplicando tres estrategias de construcción de imagen: básica, optimizada y multi-stage.

---

## Tabla de contenidos

- [Descripción](#descripción)
- [Arquitectura del proyecto](#arquitectura-del-proyecto)
- [Tecnologías utilizadas](#tecnologías-utilizadas)
- [Requisitos previos](#requisitos-previos)
- [Instalación y ejecución](#instalación-y-ejecución)
- [Comparativa de imágenes Docker](#comparativa-de-imágenes-docker)
- [Endpoints de la API](#endpoints-de-la-api)
- [Gestión de contenedores](#gestión-de-contenedores)
- [Persistencia de datos](#persistencia-de-datos)
- [Errores frecuentes y soluciones](#errores-frecuentes-y-soluciones)
- [Conceptos aplicados](#conceptos-aplicados)
- [Autora](#autora)

---

## Descripción

Este proyecto forma parte de la práctica calificada del laboratorio de **Desarrollo de Soluciones en la Nube **. El objetivo es construir y containerizar una aplicación funcional aplicando buenas prácticas de Docker, incluyendo:

- Imagen base estándar (`python:3.11-slim`)
- Imagen optimizada con Alpine Linux
- Multi-stage build para la imagen más ligera posible

La aplicación expone una interfaz web donde el usuario puede pegar una URL de Instagram (u otras redes) y descargar el video directamente desde el navegador.

---

## Arquitectura del proyecto

```
instagram-downloader/
│
├── app.py                   # Aplicación Flask (backend + frontend embebido)
├── requirements.txt         # Dependencias Python
│
├── Dockerfile               # Imagen básica (python:3.11-slim)
├── Dockerfile.optimizado    # Imagen optimizada (python:3.11-alpine)
├── Dockerfile.multistage    # Multi-stage build (imagen mínima)
│
├── downloads/               # Directorio donde se guardan los videos descargados
│   └── historial.json       # Registro de descargas (título, fecha, archivo)
│
└── README.md
```

---

## Tecnologías utilizadas

| Tecnología | Versión | Rol |
|---|---|---|
| Python | 3.11 | Lenguaje principal |
| Flask | latest | Framework web / API REST |
| yt-dlp | latest | Motor de descarga de videos |
| Docker | — | Containerización |
| Alpine Linux | 3.11 | Base de imágenes optimizadas |

---

## Requisitos previos

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) instalado y corriendo
- Conexión a internet
- Puerto `5000` disponible en el sistema

---

## Instalación y ejecución

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/instagram-downloader.git
cd instagram-downloader
```

---

### 2. Crear el directorio de descargas

Este paso es necesario para que Docker pueda montar el volumen correctamente.

```bash
# En Windows (PowerShell o CMD)
mkdir downloads

# En Linux / Mac
mkdir -p downloads
```

---

### 3. Verificar que Docker está corriendo

```bash
docker --version
```

Deberías ver algo como: `Docker version 24.x.x`. Si no, abre Docker Desktop y espera a que inicie.

---

### 4. Construir las imágenes

Debes estar dentro de la carpeta del proyecto (`cd instagram-downloader`) antes de ejecutar estos comandos.

#### Versión básica — `Dockerfile`
Usa `python:3.11-slim` (Debian). Imagen estándar sin optimizaciones adicionales.

```bash
docker build -t ig-downloader:v1.0 .
```

#### Versión optimizada — `Dockerfile.optimizado`
Usa `python:3.11-alpine`. Imagen más liviana con usuario no-root por seguridad.

```bash
docker build -f Dockerfile.optimizado -t ig-downloader:v2.0-alpine .
```

#### Versión multi-stage — `Dockerfile.multistage`
Separa la etapa de compilación de la imagen final. Resultado: imagen mínima sin herramientas de build.

```bash
docker build -f Dockerfile.multistage -t ig-downloader:v3.0-multistage .
```

> Puedes construir las tres o solo la que necesitas. Para probar la app basta con la versión básica (`v1.0`).

---

### 5. Ejecutar el contenedor

```bash
docker run -d -p 5000:5000 --name ig-container ig-downloader:v1.0
```

Verificar que está corriendo:

```bash
docker ps
```

Deberías ver `ig-container` en la lista con estado `Up`.

---

### 6. Abrir la aplicación

Abre tu navegador y entra a:

```
http://localhost:5000
```

Pega la URL del video → clic en **Descargar** → descarga el archivo.

---

### 7. Ver los logs (opcional)

Si algo no funciona, revisa los logs del contenedor:

```bash
docker logs ig-container
```

---

## Comparativa de imágenes Docker

| Imagen | Base | Tamaño aprox. | Usuario seguro | Multi-stage |
|---|---|---|---|---|
| `ig-downloader:v1.0` | `python:3.11-slim` | ~180 MB | No | No |
| `ig-downloader:v2.0-alpine` | `python:3.11-alpine` | ~80 MB | Sí (`appuser`) | No |
| `ig-downloader:v3.0-multistage` | `python:3.11-alpine` | ~50 MB | Sí (`appuser`) | Sí |

Para ver el tamaño real después de construir:

```bash
docker images | grep ig-downloader
```

---

## Endpoints de la API

| Método | Ruta | Descripción |
|---|---|---|
| `GET` | `/` | Interfaz web principal |
| `POST` | `/download` | Recibe URL y descarga el video |
| `GET` | `/downloads/<filename>` | Sirve el archivo descargado |
| `GET` | `/history` | Devuelve el historial de descargas en JSON |

**Ejemplo — body del POST `/download`:**

```json
{
  "url": "https://www.instagram.com/p/XXXXXXX/"
}
```

**Respuesta exitosa:**

```json
{
  "success": true,
  "filename": "nombre_del_video.mp4"
}
```

---

## Gestión de contenedores

```bash
# Ver contenedores activos
docker ps

# Ver logs en tiempo real
docker logs -f ig-container

# Detener el contenedor
docker stop ig-container

# Eliminar el contenedor
docker rm ig-container

# Detener y eliminar en un paso
docker rm -f ig-container

# Ver historial de capas de la imagen
docker history ig-downloader:v1.0

# Inspeccionar la imagen
docker inspect ig-downloader:v1.0

# Comparar tamaños de todas las versiones
docker images | grep ig-downloader
```

---

## Persistencia de datos

Por defecto, los videos descargados se guardan **dentro del contenedor** en `/app/downloads`. Si el contenedor se elimina, los archivos se pierden.

Para persistir los archivos en tu máquina, primero crea la carpeta `downloads/` (paso 2) y luego ejecuta con volumen:

```bash
# Windows — ruta absoluta (recomendado, reemplaza con tu ruta real)
docker run -d -p 5000:5000 -v C:\Users\TU-USUARIO\instagram-downloader\downloads:/app/downloads --name ig-container ig-downloader:v1.0

# Windows (PowerShell) — ruta relativa
docker run -d -p 5000:5000 -v ${PWD}/downloads:/app/downloads --name ig-container ig-downloader:v1.0

# Linux / Mac
docker run -d -p 5000:5000 -v $(pwd)/downloads:/app/downloads --name ig-container ig-downloader:v1.0
```

Esto sincroniza la carpeta `downloads/` local con la del contenedor. Los archivos quedan en tu PC aunque elimines el contenedor.

---

## Errores frecuentes y soluciones

**Puerto ya en uso**
```
Error: Bind for 0.0.0.0:5000 failed: port is already allocated
```
```bash
docker stop ig-container
docker rm ig-container
# O usa otro puerto: -p 5001:5000
```

---

**Nombre de contenedor duplicado**
```
Error: The container name "/ig-container" is already in use
```
```bash
docker rm -f ig-container
```

---

**No se puede eliminar la imagen**
```
Error: image is being used by a running container
```
```bash
docker rm -f ig-container
docker rmi ig-downloader:v1.0
```

---

**Video privado o sin soporte**

Algunos videos de Instagram requieren cookies de sesión o no son públicos. En ese caso yt-dlp retorna un error que la app muestra en pantalla.

---

## Conceptos aplicados

**Dockerfile y capas:** cada instrucción (`FROM`, `RUN`, `COPY`, etc.) genera una capa. Las capas se cachean, acelerando builds futuros si no cambian.

**Alpine Linux:** distribución Linux minimalista (~5 MB base). Reduce el tamaño de la imagen final significativamente respecto a Debian/Ubuntu.

**Multi-stage builds:** separa la etapa de build (donde se compilan dependencias) de la imagen final. La imagen final solo contiene lo necesario para ejecutar la aplicación, sin compiladores ni herramientas de desarrollo.

**Usuario no-root:** crear un usuario `appuser` sin privilegios de sistema reduce la superficie de ataque si el contenedor es comprometido.

**Volúmenes:** permiten compartir datos entre el host y el contenedor, y persistir archivos más allá del ciclo de vida del contenedor.

**.dockerignore:** excluye archivos innecesarios del contexto de build (`__pycache__`, `.git`, `.vscode`, etc.), reduciendo el tamaño del contexto y acelerando la construcción.

---

## Autora

**Mayela Ticona**
Curso: Desarrollo de Soluciones en la Nube — 5C24 
Laboratorio: Contenedores Docker
