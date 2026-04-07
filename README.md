# 📥 Instagram Video Downloader con Docker

## 🚀 Descripción

Este proyecto es una aplicación web desarrollada en **Python con Flask** que permite descargar videos de Instagram mediante una URL.
La aplicación está **containerizada con Docker**, aplicando buenas prácticas como optimización de imágenes y multi-stage builds.

---

## 🛠️ Tecnologías utilizadas

* Python 3.11
* Flask
* yt-dlp
* Docker

---

## 📂 Estructura del proyecto

```
instagram-examen/
│
├── app.py
├── requirements.txt
├── Dockerfile
├── Dockerfile.optimizado
├── Dockerfile.multistage
└── README.md
```

---

## ⚙️ Instalación y ejecución

### 🔹 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/instagram-downloader.git
cd instagram-downloader
```

---

### 🔹 2. Construir la imagen Docker

#### Versión básica:

```bash
docker build -t ig-app:v1 .
```

#### Versión optimizada:

```bash
docker build -f Dockerfile.optimizado -t ig-app:v2 .
```

#### Versión multistage:

```bash
docker build -f Dockerfile.multistage -t ig-app:v3 .
```

---

### 🔹 3. Ejecutar el contenedor

```bash
docker run -d -p 5000:5000 --name ig-container ig-app:v1
```

---

### 🔹 4. Acceder a la aplicación

Abrir en el navegador:

```
http://localhost:5000
```

---

## 🎯 Funcionalidades

* ✅ Descargar videos desde Instagram
* ✅ Interfaz web amigable
* ✅ Historial de descargas (nombre y fecha)
* ✅ Alert de confirmación al descargar
* ✅ Aplicación containerizada con Docker

---

## 📦 Gestión de contenedores

### Ver contenedores

```bash
docker ps
```

### Detener contenedor

```bash
docker stop ig-container
```

### Eliminar contenedor

```bash
docker rm ig-container
```

---

## ⚠️ Problemas comunes y soluciones

### ❌ Puerto ocupado

```
port is already allocated
```

✔️ Solución:

```bash
docker stop <contenedor>
docker rm <contenedor>
```

---

### ❌ Nombre de contenedor duplicado

```
container name already in use
```

✔️ Solución:

```bash
docker rm -f ig-container
```

---

### ❌ No se puede eliminar imagen

✔️ Porque está siendo usada por un contenedor
✔️ Primero eliminar el contenedor

---

## 💾 Persistencia de archivos

Por defecto, los videos se guardan dentro del contenedor.
Para guardarlos en tu PC:

```bash
docker run -d -p 5000:5000 -v ${PWD}:/app --name ig-container ig-app:v1
```

---

## 🧠 Conceptos aprendidos

* Creación de contenedores Docker
* Uso de Dockerfile
* Optimización con Alpine
* Multi-stage builds
* Manejo de puertos y contenedores
* Uso de volúmenes

---

## 📌 Conclusión

En este proyecto se logró desarrollar y containerizar una aplicación funcional para la descarga de videos de Instagram, aplicando buenas prácticas de Docker como optimización de imágenes y separación de etapas. Esto demuestra la importancia de Docker en el desarrollo moderno y despliegue de aplicaciones.

---

## 👩‍💻 Autor
Mayela Ticona 
Proyecto desarrollado como práctica de laboratorio de contenedores y microservicios.
