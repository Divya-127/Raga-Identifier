from django.contrib import admin
from django.urls import path
from MyAPI import views

urlpatterns = [
    path('',views.index_page),
    path('predict',views.predict_raga),
]
