from django.urls import path
from . import views

app_name = 'properties'  # Namespace for URL naming

urlpatterns = [
    path('', views.property_list, name='property_list'),
    path('create/', views.property_create, name='property_create'),
    path('<str:property_id>/', views.property_detail, name='property_detail'),
]