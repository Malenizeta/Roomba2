import requests

SERVER_URL = "http://127.0.0.1:8000"

def registrar_usuario():
    print("Registrar usuario:")
    username = input("Ingrese un nombre de usuario: ")
    password = input("Ingrese una contraseña: ")

    try:
        response = requests.post(f"{SERVER_URL}/registrar_usuario/", json={
            "username": username,
            "password": password,
        })

        if response.status_code == 200:
            data = response.json()
            print(data["message"])
            return iniciar_sesion()
        else:
            print(f"Error: {response.json().get('error', 'Error desconocido')}")
    except requests.RequestException as e:
        print(f"Error al conectar con el servidor: {e}")

def iniciar_sesion():
    print("Iniciar sesión:")
    username = input("Ingrese su nombre de usuario: ")
    password = input("Ingrese su contraseña: ")

    try:
        response = requests.post(f"{SERVER_URL}/iniciar_sesion/", json={
            "username": username,
            "password": password
        })

        if response.status_code == 200:
            data = response.json()
            print("Inicio de sesión exitoso.")
            return data["user_id"]
        else:
            print(f"Error: {response.json().get('error', 'Error desconocido')}")
            return None
    except requests.RequestException as e:
        print(f"Error al conectar con el servidor: {e}")
        return None
    
def menu_autenticacion():
    while True:
        print("Bienvenido a Roomba y el Desafío del Papel Pintado")
        print("1. Iniciar sesión")
        print("2. Registrarse")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            usuario = iniciar_sesion()
            if usuario:
                print(f"Inicio de sesión exitoso. Bienvenido, usuario {usuario}!")
                return usuario
        elif opcion == "2":
            usuario = registrar_usuario()
            if usuario:
                print(f"Registro exitoso. Bienvenido, usuario {usuario}!")
                return usuario
        else:
            print("Opción no válida. Intente de nuevo.")