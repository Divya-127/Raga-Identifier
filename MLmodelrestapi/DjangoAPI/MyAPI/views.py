from django.shortcuts import render
from rest_framework import viewsets
from .models import Task
from .Serializers import TaskSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render
import math
import librosa
from keras.models import model_from_json
from pathlib import Path
import numpy as np
import os
from django.core.files.storage import FileSystemStorage

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all().order_by('-date_created')
    serializer_class = TaskSerializer

class DueTaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all().order_by('-date_created')
    serializer_class = TaskSerializer

class CompletedTaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all().order_by('-date_created')
    serializer_class = TaskSerializer

@api_view(['GET'])
def index_page(request):
    return_data = {
        "error":"0",
        "message":"Successful"
    }
    return Response(return_data)

@api_view(['POST'])
def predict_raga(request):
    BASE_DIR = Path(__file__).resolve().parent.parent
    try:
        file = request.FILES.get('file',None)
        fs = FileSystemStorage()
        name = fs.save(file.name,file)
        name.replace(" ","")
        url = fs.url(name=name)
        fields = [file]
        if not None in fields:
            file = file
            SAMPLE_RATE = 22050
            DURATION = 30
            SAMPLES_PER_TRACK = SAMPLE_RATE * DURATION
            num_segments = 1
            hop_length = 512
            n_fft = 2048
            n_mfccs = 13

            data = {
                "mfcc": []
            }
            num_samples_per_segment = int(SAMPLES_PER_TRACK / num_segments)
            expected_num_mfcc_vectors_per_segment = math.ceil(num_samples_per_segment / hop_length)
            #print(BASE_DIR)
            file = "E:\MLmodelrestapi\DjangoAPI"+url
            print(file)
            signal, sr = librosa.load(file, sr=SAMPLE_RATE)
            for s in range(num_segments):
                start_sample = num_samples_per_segment * s  # s=0 -> 0
                finish_sample = start_sample + num_samples_per_segment

                mfcc = librosa.feature.mfcc(signal[start_sample:finish_sample],
                                            sr=sr,
                                            n_mfcc=n_mfccs,
                                            n_fft=n_fft,
                                            hop_length=hop_length)
                mfcc = mfcc.T

                if len(mfcc) == expected_num_mfcc_vectors_per_segment:
                    data["mfcc"].append(mfcc)

            X = data["mfcc"]
            with open('MyAPI/model_num.json', 'r') as f:
                model = model_from_json(f.read())
            model.load_weights('MyAPI/model_num.h5')
            for i in range(0,len(X)):
                prediction = 'none'
                predicted_index = predict(X[i],model)
                print(predicted_index)
                print(predicted_index)
                if predicted_index==0:
                    prediction = 'bageshree'
                elif predicted_index ==1:
                    prediction ='bhairavi'
                elif predicted_index ==2:
                    prediction ='bhoopali'
                elif predicted_index ==3:
                    prediction ='malkauns'
                elif predicted_index ==4:
                    prediction ='sarang'
                elif predicted_index ==5:
                    prediction ='todi'
                elif predicted_index ==6:
                    prediction ='yaman'
                predictions = {
                    'error':'0',
                    'message':'Successful',
                    'prediction':prediction
                }
        else:
            predictions = {
                'error': '1',
                'message': 'Invalid params',
                'prediction': -1
            }
    except Exception as e:
        predictions = {
            'error': '2',
            'message': str(e),
            'prediction': -1
        }
    return Response(predictions)

def predict(X,model):
    X = X[np.newaxis, ...]  # array shape (1, 185, 13, 1)
    prediction = model.predict(X)
    print(prediction)
    predicted_index = np.argmax(prediction, axis=1)
    return predicted_index