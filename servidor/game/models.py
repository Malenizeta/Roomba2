from django.db import models
from django.contrib.auth.models import User

class Level(models.Model):
    inicio = models.JSONField()  
    fin = models.JSONField()    
    obstaculos = models.JSONField()  
    tile_image = models.CharField(max_length=100)  


class PlayerProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="progress")
    level_id = models.IntegerField()  # ID del nivel
    painted_cells = models.JSONField()  # Celdas pintadas en el nivel
    completado = models.BooleanField(default=False)  # Si el nivel está completado