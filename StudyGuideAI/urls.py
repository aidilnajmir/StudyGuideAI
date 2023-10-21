from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload_material, name='upload_material'),  # Define a URL pattern for the root path
    path('upload/', views.upload_material, name='upload_material'),  # This line is optional
    # Add more URL patterns as needed for your app
]
