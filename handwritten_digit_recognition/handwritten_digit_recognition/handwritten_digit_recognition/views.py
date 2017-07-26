'''
Created on Jul 20, 2017

@author: aneesh.c
'''
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import status
from rest_framework.decorators import permission_classes
import os
import path
from scipy.misc import imread, imresize
from keras.preprocessing.image import img_to_array
from keras.preprocessing.image import load_img
from keras.applications import imagenet_utils
from keras.applications import VGG16
import numpy as np



@permission_classes((permissions.AllowAny,))
class TestAPI(viewsets.ViewSet):
    def create(self, request):
        file = request.FILES['file']
        file_name = str(file)
        path = os.getcwd()
        print path
        with open(path+'/'+file_name, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        image = imread(path+"/"+file_name, mode='L')
        inputShape = (224, 224)
        preprocess = imagenet_utils.preprocess_input
        Network = VGG16
        model = Network(weights="imagenet")
        resized = imresize(image, inputShape)
        image = img_to_array(resized)
        image = np.expand_dims(image, axis=0)
        image = preprocess(image)
        preds = model.predict(image)
        P = imagenet_utils.decode_predictions(preds)
        dict = {}
        for (i, (imagenetID, label, prob)) in enumerate(P[0]):
            dict[label] = prob * 100
            print("{}. {}: {:.2f}%".format(i + 1, label, prob * 100))
        return Response(dict)
