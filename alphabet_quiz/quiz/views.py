from django.http import HttpResponse
import numpy as np
from bidict import bidict
from random import choice
from tensorflow import keras
from django.shortcuts import render, redirect
from django.template import loader
import cv2

# Assuming data/ is in the root directory of your project
DATA_DIR = '../'

ENCODER = bidict({
    'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6,
    'G': 7, 'H': 8, 'I': 9, 'J': 10, 'K': 11, 'L': 12,
    'M': 13, 'N': 14, 'O': 15, 'P': 16, 'Q': 17, 'R': 18,
    'S': 19, 'T': 20, 'U': 21, 'V': 22, 'W': 23, 'X': 24,
    'Y': 25, 'Z': 26
})

def index(request):
    return render(request, "index.html")

def add_data_get(request):
    message = request.session.get('message', '')
    letter = choice(list(ENCODER.keys()))
    return render(request, "addData.html", {'letter': letter, 'message': message})

def add_data_post(request):
    label = request.POST['letter']
    labels = np.load(DATA_DIR + 'labels.npy')
    labels = np.append(labels, label)
    np.save(DATA_DIR + 'labels.npy', labels)

    pixels = request.POST['pixels'].split(',')
    img = np.array(pixels).astype(float).reshape(1, 50, 50)
    imgs = np.load(DATA_DIR + 'images.npy')
    imgs = np.vstack([imgs, img])
    np.save(DATA_DIR + 'images.npy', imgs)

    request.session['message'] = f'"{label}" added to the training dataset'
    return redirect('add_data_get')

def practice_get(request):
    
    return render(request, "practice.html", {'letter': '', 'correct': ''})

def practice_post(request):
    print ('hello')
    try:
        #letter = request.POST['letter']
        pixels = request.POST['pixels'].split(',')
        img = np.array(pixels).astype(float).reshape(1, 50, 50, 1)
        model = keras.models.load_model('letter.model')
        pred_letter = np.argmax(model.predict(img), axis=-1)
        pred_letter = ENCODER.inverse[pred_letter[0]]
        correct =pred_letter 
        return render(request, "practice.html", {'letter': '', 'correct': correct})

    except Exception as e:
        return render(request, 'error.html')
    
    
# number part here 
def practice_numb_get(request):
    
    return render(request, "practice_numb.html", {'letter': '', 'correct': ''})


# practice_numb_post is the same as practice_post part
def practice_numb_post(request):
    try:
        pixels = request.POST['pixels'].split(',')
        img = np.array(pixels).astype(float).reshape(1, 50, 50, 1)
        img_resized = cv2.resize(img[0], (28, 28)).reshape(1, 28, 28, 1)
        
        model = keras.models.load_model('chiffre.model')
        pred_letter = np.argmax(model.predict(img_resized), axis=-1)
        pred_letter = pred_letter[0] 
        correct = pred_letter 
        return render(request, "practice_numb.html", {'letter': '', 'correct': correct})
    
    except Exception as e:
        return render(request, 'error.html')
