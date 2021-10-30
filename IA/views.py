from io import StringIO
from keras.backend import relu
import tensorflow as tf 
import numpy as np
import cv2
import matplotlib.pyplot as plt
from django.conf import settings 
from django.core.files.storage import default_storage
from django.shortcuts import render 
from keras.applications import vgg16
from keras.applications.imagenet_utils import decode_predictions
from keras.preprocessing.image import img_to_array, load_img
import easyocr
from matplotlib import pyplot as plt
from PIL import Image

def index(request):
    if request.method == "POST":
        #
        # Django image API
        #
        try:
            file = request.FILES["imageFile"]
            file_name = default_storage.save(file.name, file)
            file_url = default_storage.path(file_name)
                
        except KeyError:
            return render(request, "index.html",{"datos":"ERROR"})

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
            imagen = cv2.imread(file_url)
            gray = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
            gray = cv2.blur(gray,(3,3))
            canny = cv2.Canny(gray,150,200)
            canny = cv2.dilate(canny,None,iterations=1)
            cnts,_ = cv2.findContours(canny,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

            IMAGE_PATH = file_url
            reader = easyocr.Reader(['en'], gpu=False)
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
                #imagen = Image.fromarray(cv2.resizelist[img])
                #file_name2 = default_storage.save(file.name, imagen)
                #file_url2 = default_storage.path(file_name2)
                #val = load_img(file_url2, target_size=(224, 224))

            for c in cnts:
                area = cv2.contourArea(c)
                x,y,w,h = cv2.boundingRect(c)
                epsilon = 0.09*cv2.arcLength(c,True)
                approx = cv2.approxPolyDP(c,epsilon,True)
            
                if len(approx)==4:
                    contador += 1 
                    aspect_ratio = float(w)/h
                    if aspect_ratio>2.4:
                        placa = gray[y:y+h,x:x+w]
                        img = cv2.imread(file_url)
                        custom_config = r'--oem 3 --psm 6'
            return render(request, "index.html", {"predictions": objeto, 
                                                  "datos" : "Es un carro",
                                                  "url": "http://127.0.0.1:8000/media/"+file_name,
                                                  "area":text,
                                                  "img": "",
                                                  "gris":contador,})
                                                  
        return render(request, "index.html", {"predictions": objeto,
                                              "datos" : "No es un carro",
                                              "url": "http://127.0.0.1:8000/media/"+file_name})

    return render(request, "index.html")

