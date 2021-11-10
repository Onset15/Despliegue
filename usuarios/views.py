from django.shortcuts import render
import tensorflow as tf 
import numpy as np
import cv2
from django.core.files.storage import default_storage
from django.shortcuts import render 
from keras.applications import vgg16
from keras.applications.imagenet_utils import decode_predictions
from keras.preprocessing.image import img_to_array, load_img
import easyocr
from PIL import Image
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .forms import *
from django.urls import reverse_lazy
from django.db import connection
from usuarios.models import Usuario, Vehiculo
import re, random, string

def my_custom_sql(text):
    with connection.cursor() as cursor:
        cursor.execute('''SELECT * FROM usuarios_vehiculo WHERE matricula LIKE  "'''+text+'''"''')
        row = cursor.fetchone()
    if(row):
        with connection.cursor() as cursor2:
            cursor2.execute("SELECT * FROM usuarios_usuario WHERE id_usuarios = %s", [row[5]])
            row2 = cursor2.fetchone()
        return row, row2
    return None,None

def index(request):
    if request.method == "POST":
        # Django image API
        try:
            file = request.FILES["imageFile"]

        except KeyError:
            return render(request, "index.html",{"datos":None})

        datosUsuario = None
        file = request.FILES["imageFile"]
        file_name = default_storage.save(file.name, file)
        file_url = default_storage.path(file_name)

        image = load_img(file_url, target_size=(224, 224))
        numpy_array = img_to_array(image)
        image_batch = np.expand_dims(numpy_array, axis=0)
        processed_image = vgg16.preprocess_input(image_batch.copy())

        model = tf.keras.applications.resnet50.ResNet50()
        predictions = model.predict(processed_image)
        label = decode_predictions(predictions, top=1)
        contador = 0
        objeto = label[0][0][1]    
        
        if 'car' in objeto or 'pickup' in objeto or 'truck' in objeto or 'grille' in objeto or "cab" in objeto or 'minivan' in objeto or 'jeep' in objeto or 'cuv' in objeto or "van" in objeto or "super_car" in objeto or "micro" in objeto or "cabriolet" in objeto:
            placa = []
            IMAGE_PATH = file_url
            reader = easyocr.Reader(['es'], gpu=False)
            result = reader.readtext(IMAGE_PATH)
            text = ""
            if result:
                top_left = tuple(result[0][0][0])
                bottom_right = tuple(result[0][0][2])
                text = result[0][1]
                font = cv2.FONT_HERSHEY_SIMPLEX
                img = cv2.imread(IMAGE_PATH)
                img = cv2.rectangle(img,top_left,bottom_right,(0,255,0),5)
                img = cv2.putText(img,text,top_left,font,.5,(255,255,255),2,cv2.LINE_AA)
                img2 = cv2.imread(IMAGE_PATH)
                crop = img2[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]
                imagen = Image.fromarray(crop)
                name = random.choice(string.ascii_letters)
                imagen.save("media/"+name+file.name)
                
                #Creando la consulta para la matricula
                text=re.sub("\!|\'|\?|\]|\[|\}|\{|\)|\(","",text)
                datosVehiculo, datosUsuario = my_custom_sql(text.strip())

            if datosUsuario != None:
                return render(request, "index.html", {"predictions": objeto, 
                                                    "datos" : "es un carro",
                                                    "url": "http://127.0.0.1:8000/media/"+file_name,
                                                    "placa": "http://127.0.0.1:8000/media/"+name+file.name,
                                                    "area":text,
                                                    "estado": "True",
                                                    "gris":contador,
                                                    "datosVehiculo":datosVehiculo[1],
                                                    "datosVehiculoModelo":datosVehiculo[2],
                                                    "datosVehiculoColor":datosVehiculo[3],
                                                    "datosVehiculoAnio":datosVehiculo[4],
                                                    "datosUsuarioNombres":datosUsuario[1],
                                                    "datosUsuarioApellidos":datosUsuario[2],
                                                    "datosUsuarioDireccion":datosUsuario[3],
                                                    "datosUsuarioTelefono":datosUsuario[4],
                                                    "datosUsuarioDui":datosUsuario[5],
                                                    "datosUsuarioLicencia":datosUsuario[7],
                                                    "mensaje":"Los datos relacionados son"})
            else:
                return render(request, "index.html", {"predictions": objeto, 
                                                    "datos" : "es un carro",
                                                    "url": "http://127.0.0.1:8000/media/"+file_name,
                                                    "area":text,
                                                    "estado": "True",
                                                    "gris":contador,
                                                    "error":"No posee datos relacionados",
                                                    "datosVehiculo":None,
                                                    "mensaje":"Es vehiculo pero no posee matricula"})
                                                  
        return render(request, "index.html", {"predictions": objeto,
                                              "datos" : "no es un carro",
                                              "estado": "True",
                                              "url": "http://127.0.0.1:8000/media/"+file_name,
                                              "datosVehiculo":None,
                                              "mensaje":"No es vehiculo y no posee matricula"})

    return render(request, "index.html")

#Modelo para listar Usuarios 
class UsuariosListar(ListView):
    model = Usuario
    template_name= 'listarUsuarios.html'

#Modelo para listar Vehiculos 
class VehiculosListar(ListView):
    model = Vehiculo
    template_name= 'listarVehiculos.html'

#Modelo para crear Usuarios
class UsuariosCrear(CreateView):
    template_name = 'Usuarios/crear.html'
    form_class = UsuariosForm
    sucess_messege = 'Exito'
    success_url = reverse_lazy('usuarios:listar_usuarios')

#Modelo para crear Vehiculos 
class VehiculosCrear(CreateView):
    template_name = 'Vehiculos/crear.html'
    form_class = VehiculosForm
    sucess_messege = 'Exito'
    success_url = reverse_lazy('usuarios:listar_vehiculos')

#Modelo para modificar Usuarios
class UsuariosModificar(UpdateView):
    model = Usuario
    template_name = 'Usuarios/crear.html'
    form_class = UsuariosForm
    sucess_messege = 'Exito'
    success_url = reverse_lazy('usuarios:listar_usuarios')

#Modelo para modificar Vehiculos 
class VehiculosModificar(UpdateView):
    model = Vehiculo
    template_name = 'Vehiculos/crear.html'
    form_class = VehiculosForm
    sucess_messege = 'Exito'
    success_url = reverse_lazy('usuarios:listar_vehiculos')

class UsuariosEliminar(DeleteView):
    model = Usuario
    template_name = "Usuarios/eliminar.html"
    sucess_messege = 'Exito al elimiar usuario'
    success_url = reverse_lazy('usuarios:listar_usuarios')

class VehiculosEliminar(DeleteView):
    model = Vehiculo
    template_name = "Vehiculos/eliminar.html"
    sucess_messege = 'Exito al elimiar vehiculo'
    success_url = reverse_lazy('usuarios:listar_vehiculos')