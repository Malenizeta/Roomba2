# Roomba y el Desafío del Papel Pintado

¡Bienvenido a **Roomba y el Desafío del Papel Pintado**! Este es un juego interactivo en el que controlas una Roomba para pintar un área mientras esquivas obstáculos. El proyecto incluye un servidor que gestiona los niveles del juego y los usuarios registrados.

## Descripción del Proyecto

Este proyecto está dividido en dos partes principales:

1. **Servidor**:
   - Gestiona los niveles del juego.
   - Permite registrar usuarios y manejar la autenticación.
   - Proporciona una API para cargar niveles y listar usuarios registrados.
   - Ofrece una interfaz web para explorar los niveles disponibles y los usuarios registrados.

2. **Cliente**:
   - Es el juego en sí, donde puedes controlar la Roomba para completar los niveles.
   - Carga los niveles desde el servidor mediante la API.
   - Incluye un sistema de autenticación para iniciar sesión o registrarse antes de jugar.

## Requisitos Previos

Asegúrate de tener instalado lo siguiente en tu sistema:
- Python 3.8 o superior
- Pygame (para el cliente)
- Las dependencias listadas en `requirements.txt`

## Instalación

1. Clona este repositorio en tu máquina local:
   ```bash
   git clone <URL_DEL_REPOSITORIO>
   cd Roomba2
   ```

2. Instala las dependencias necesarias:
   ```bash
   pip install -r requirements.txt
   ```

3. Configura la base de datos de Django:
   ```bash
   python manage.py migrate
   ```

## Ejecución del Proyecto

### 1. Ejecutar el Servidor
El servidor es necesario para gestionar los niveles y los usuarios. Para iniciarlo, ejecuta:
```bash
python manage.py runserver
```
Esto iniciará el servidor en `http://127.0.0.1:8000/`.

### 2. Ejecutar el Cliente
El cliente es el juego. Para iniciarlo, ejecuta:
```bash
python -m cliente.main
```

## Funcionalidades del Servidor

- **Gestión de Niveles**: El servidor proporciona una API para cargar los niveles del juego.
- **Gestión de Usuarios**: Permite registrar nuevos usuarios e iniciar sesión.
- **Interfaz Web**:
  - Ver los niveles disponibles con imágenes.
  - Listar los usuarios registrados.
    ![Captura de pantalla 2025-04-05 185221](https://github.com/user-attachments/assets/8680d5d8-0eff-4d04-b56c-63808d0627a9)
    ![Captura de pantalla 2025-04-05 185228](https://github.com/user-attachments/assets/8ef8da92-d155-4e93-9cc8-b1c2ebabc9f4)
    ![Captura de pantalla 2025-04-05 185237](https://github.com/user-attachments/assets/1f175af8-ab2d-4d04-ab3c-de4ba99c9da3)

## Funcionalidades del Cliente

- **Juego Interactivo**: Controla la Roomba para pintar el área mientras esquivas obstáculos.
- **Autenticación**: Inicia sesión o regístrate antes de jugar.
- **Carga de Niveles**: Obtiene los niveles dinámicamente desde el servidor.

## Estructura del Proyecto

```
Roomba2/
├── cliente/
│   ├── __init__.py      # Indica que esta carpeta es un paquete Python
│   ├── auth.py          # Funciones de autenticación (registro e inicio de sesión)
│   ├── game.py          # Lógica del juego
│   ├── level.py         # Clase Level y lógica de niveles
│   ├── main.py          # Punto de entrada del cliente
│   ├── utils.py         # Funciones auxiliares
│   ├── const.py         # Constantes globales del cliente (dimensiones, colores, etc.)
├── servidor/
│   ├── game/
│   │   ├── views.py     # Vistas del servidor
│   │   ├── urls.py      # Rutas del servidor
│   ├── settings.py      # Configuración de Django
│   ├── ...
├── manage.py            # Comando principal de Django
├── requirements.txt     # Dependencias del proyecto
├── README.md            # Este archivo
```

## API del Servidor

El servidor expone las siguientes rutas principales:

- **`POST /registrar_usuario/`**: Registra un nuevo usuario.
- **`POST /iniciar_sesion/`**: Inicia sesión con un usuario existente.
- **`GET /api/levels/`**: Devuelve los niveles disponibles.
- **`GET /usuarios_registrados/`**: Muestra una lista de usuarios registrados.

¡Disfruta jugando a **Roomba y el Desafío del Papel Pintado**!
