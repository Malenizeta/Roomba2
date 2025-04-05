from django.http import JsonResponse
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from django.contrib.auth import authenticate, login

def home(request):
    # Obtenemos todos los usuarios registrados
    usuarios = User.objects.all()
    usuarios_html = "".join(
        f"<li>ID: {usuario.id}, Username: {usuario.username}, Fecha de registro: {usuario.date_joined.strftime('%Y-%m-%d %H:%M:%S')}</li>"
        for usuario in usuarios
    )

    html_content = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Servidor del Juego</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                text-align: center;
                background-color: #f4f4f9;
                color: #333;
                margin: 0;
                padding: 0;
            }}
            header {{
                background-color: #87abed;
                color: white;
                padding: 20px 0;
            }}
            h1 {{
                margin: 0;
            }}
            main {{
                padding: 20px;
            }}
            a {{
                color: #87abed;
                text-decoration: none;
                font-weight: bold;
            }}
            a:hover {{
                text-decoration: underline;
            }}
            footer {{
                margin-top: 20px;
                font-size: 0.9em;
                color: #666;
            }}
            ul {{
                text-align: left;
                display: inline-block;
            }}
        </style>
    </head>
    <body>
        <header>
            <h1>Bienvenido al Servidor del Juego</h1>
        </header>
        <main>
            <p>Bienvenido al servidor del juego. Aquí puedes explorar los niveles disponibles y ver la lista de usuarios registrados.</p>
            <p>Selecciona una de las siguientes opciones:</p>
            <ul>
                <li><a href="/niveles_disponibles/">Ver niveles disponibles</a></li>
                <li><a href="/usuarios_registrados/">Usuarios Registrados</a></li>
            </ul>
        </main>
        <footer>
            <p>Servidor gestionado por Malen Izeta</p>
        </footer>
    </body>
    </html>
    """
    return HttpResponse(html_content)

# Definición simple de la clase Level para representar los niveles.
class Level:
    def __init__(self, player_start, player_end, obstaculos, tile_image):
        self.player_start = player_start
        self.player_end = player_end
        self.obstaculos = obstaculos
        self.tile_image = tile_image

# Función que convierte un objeto Level en un diccionario serializable a JSON.
def serialize_level(level):
    return {
        "inicio": list(level.player_start),  # Convertimos la tupla a lista
        "fin": list(level.player_end),
        "obstaculos": [
            {
                # Convertimos el set de celdas a una lista de listas
                "cells": [list(cell) for cell in obstacle["cells"]],
                "image": obstacle["image"]
            }
            for obstacle in level.obstaculos
        ],
        "tile_image": level.tile_image
    }

# Vista que devuelve los niveles en formato JSON.
def cargar_niveles(request):
    user = request.user
    levels = [
        Level(
            (0, 0), (5, 10), 
            [
                {"cells": {(2, 3), (2, 4), (2, 5), (3, 3), (3, 4), (3, 5)}, "image": "obstacle1.jpg"},
                {"cells": {(1, 7), (1, 8), (2, 7), (2, 8)}, "image": "obstacle2.jpg"},
                {"cells": {(0, 10), (0, 11), (1, 10), (1, 11), (2, 10), (2, 11)}, "image": "obstacle3.jpg"},
                {"cells": {(3, 0), (3, 1), (4, 0), (4, 1), (5, 0), (5, 1)}, "image": "obstacle4.jpg"}
            ], 
            "Tile1.jpg"
        ),

        Level(
            (0, 0), (0, 9), 
            [
                {"cells": {(2, 3), (2, 4), (3, 3), (3, 4), (4, 3), (4, 4), (5, 3), (5, 4)}, "image": "obstacle8.jpg"},
                {"cells": {(2, 9), (2, 10), (3, 9), (3, 10), (4, 9), (4, 10)}, "image": "obstacle9.jpg"},
                {"cells": {(0, 7), (0, 8), (1, 7), (1, 8)}, "image": "obstacle10.jpg"}
            ], 
            "Tile3.jpg"
        ),

        Level(
            (3, 2), (1, 10), 
            [
                {"cells": {(1, 3), (1, 4), (1, 5), (2, 3), (2, 4), (2, 5), (3, 3), (3, 4), (3, 5)}, "image": "obstacle11.jpg"},
                {"cells": {(3, 7), (3, 8), (3, 9), (3, 10), (4, 7), (4, 8), (4, 9), (4, 10)}, "image": "obstacle12.jpg"}
            ], 
            "Tile4.jpg"
        ),
        
        Level(
            (2, 4), (1, 10), 
            [ 
                {"cells": {(1, 2), (2, 2), (3, 2), (4, 2), (1, 3), (2, 3), (3, 3), (4, 3)}, "image": "obstacle5.jpg"},
                {"cells": {(2, 6), (3, 6)}, "image": "obstacle6.jpg"},
                {"cells": {(3, 9), (3, 10), (4, 9), (4, 10)}, "image": "obstacle7.jpg"}
            ], 
            "Tile2.jpg"
        ),
    ]
    # Serializamos cada nivel y lo devolvemos como JSON.
    data = [serialize_level(level) for level in levels]
    return JsonResponse(data, safe=False)

# # Creo una vista para registrar usuarios
@csrf_exempt
def registrar_usuario(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data.get("username")
            password = data.get("password")

            if not username or not password:
                return JsonResponse({"error": "El nombre de usuario y la contraseña son obligatorios."}, status=400)

            if User.objects.filter(username=username).exists():
                return JsonResponse({"error": "El nombre de usuario ya está en uso."}, status=400)

            user = User.objects.create_user(username=username, password=password)
            return JsonResponse({
               "message": "Usuario registrado exitosamente. Redirigiendo a inicio de sesión.",
                "redirect_to": "/iniciar_sesion/"})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Método no permitido."}, status=405)

# # Creo otra vista para que puedan iniciar sesión
@csrf_exempt
def iniciar_sesion(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data.get("username")
            password = data.get("password")

            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse({"message": "Inicio de sesión exitoso.", "user_id": user.id})
            else:
                return JsonResponse({"error": "Credenciales inválidas."}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Método no permitido."}, status=405)

# Vista para que aparezca una lista de los usuarios registrados

@csrf_exempt
def listar_usuarios(request):
    if request.method == "GET":
        try:
            # Obtenemos todos los usuarios
            usuarios = User.objects.all()
            # Serializamos los datos de los usuarios
            data = [
                {
                    "id": usuario.id,
                    "username": usuario.username,
                    "date_joined": usuario.date_joined.strftime("%Y-%m-%d %H:%M:%S"),
                }
                for usuario in usuarios
            ]
            return JsonResponse({"usuarios": data}, safe=False)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Método no permitido."}, status=405)

def usuarios_registrados(request):
    # Obtenemos todos los usuarios registrados
    usuarios = User.objects.all()
    usuarios_html = "".join(
        f"<li>ID: {usuario.id}, Username: {usuario.username}, Fecha de registro: {usuario.date_joined.strftime('%Y-%m-%d %H:%M:%S')}</li>"
        for usuario in usuarios
    )

    html_content = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Usuarios Registrados</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                text-align: center;
                background-color: #f4f4f9;
                color: #333;
                margin: 0;
                padding: 0;
            }}
            header {{
                background-color: #87abed;
                color: white;
                padding: 20px 0;
            }}
            h1 {{
                margin: 0;
            }}
            main {{
                padding: 20px;
            }}
            ul {{
                text-align: left;
                display: inline-block;
            }}
        </style>
    </head>
    <body>
        <header>
            <h1>Usuarios Registrados</h1>
        </header>
        <main>
            <ul>
                {usuarios_html}
            </ul>
            <a href="/">Volver a la página principal</a>
        </main>
    </body>
    </html>
    """
    return HttpResponse(html_content)

def niveles_disponibles(request):
    # Lista de imágenes de los niveles
    imagenes = [
        "Tile1.jpg",
        "Tile2.jpg",
        "Tile3.jpg",
        "Tile4.jpg",
    ]

    # Generar HTML para mostrar las imágenes
    imagenes_html = "".join(
        f'<img src="/static/{imagen}" alt="Nivel {i+1}" style="width: 200px; height: auto; margin: 10px;">'
        for i, imagen in enumerate(imagenes)
    )

    html_content = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Niveles Disponibles</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                text-align: center;
                background-color: #f4f4f9;
                color: #333;
                margin: 0;
                padding: 0;
            }}
            header {{
                background-color: #87abed;
                color: white;
                padding: 20px 0;
            }}
            h1 {{
                margin: 0;
            }}
            main {{
                padding: 20px;
            }}
            img {{
                margin: 10px;
                border: 2px solid #87abed;
                border-radius: 10px;
            }}
        </style>
    </head>
    <body>
        <header>
            <h1>Niveles Disponibles</h1>
        </header>
        <main>
            <div>
                {imagenes_html}
            </div>
            <a href="/">Volver a la página principal</a>
        </main>
    </body>
    </html>
    """
    return HttpResponse(html_content)