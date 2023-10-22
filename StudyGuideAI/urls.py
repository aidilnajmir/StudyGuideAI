from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload_material, name='upload_material'),  # Define a URL pattern for the root path
    path('upload/', views.upload_material, name='upload_material'),  # This line is optional
    path('download_pdf/', views.download_pdf, name='download_pdf'),
    path('download_pdf2/', views.download_pdf2, name='download_pdf2'),

    # Add more URL patterns as needed for your app
]
