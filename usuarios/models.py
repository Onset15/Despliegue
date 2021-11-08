from django.db import models

# Create your models here.
class Usuario(models.Model):
    id_usuarios = models.AutoField(primary_key=True)
    nombres = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=50)
    direccion = models.TextField()
    telefono = models.CharField(max_length=9)
    dui = models.CharField(max_length=10)
    fechaNacimiento = models.DateField()
    licencia = models.CharField(max_length=9)

    def __str__(self):
        return self.nombres 


#Modelo de Vehiculo
class Vehiculo(models.Model):
    id_vehiculo = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    matricula = models.CharField(max_length=12)
    modelo = models.CharField(max_length=50) 
    color = models.CharField(max_length=50)
    anio = models.DateField() #Año en el que se fabrico el vehiculo

    def __str__(self):
        return self.matricula
