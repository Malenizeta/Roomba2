import json
import os
from django.shortcuts import render

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NIVELES_PATH = os.path.join(BASE_DIR, "niveles.json")

# Función para leer niveles
def cargar_niveles():
    with open(NIVELES_PATH, "r") as file:
        return json.load(file)

# Función para guardar niveles
def guardar_niveles(niveles):
    with open(NIVELES_PATH, "w") as file:
        json.dump(niveles, file, indent=4)
