"""
URL Configuration for "upload_img" application
"""
from django.urls import path

from .views import index, upload_img_form, change_size_from

urlpatterns = [
    path('', index),
    path('upload/', upload_img_form),
    path('image/<uuid:imguuid>/', change_size_from, name='image-uuid'),
]