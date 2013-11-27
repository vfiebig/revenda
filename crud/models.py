'''
from django.db import models

class Veiculo(models.Model):
    ano = models.IntegerField()
    fabricante = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)
    #foto = models.ImageField(upload_to='documents/%Y/%m/%d')

    def __unicode__(self):
        return str(self.fabricante)+" "+str(self.modelo)+" ("+str(self.ano)+")"
'''
from mongoengine import *

connect('revenda')

class Veiculo(Document):
    ano = IntField()
    fabricante = StringField(max_length=100)
    modelo = StringField(max_length=100)
    foto = ImageField(size=(250, 250, True))

    @property
    def gridfile_attr(self):
        return str(self.foto.grid_id)

    @property
    def pic(self):
        return self.foto.read()
