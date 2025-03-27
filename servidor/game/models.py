from django.db import models

class Level(models.Model):
    inicio = models.JSONField()  
    fin = models.JSONField()    
    obstaculos = models.JSONField()  
    tile_image = models.CharField(max_length=100)  


