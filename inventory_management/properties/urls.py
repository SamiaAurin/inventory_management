from django.urls import path
from . import views

app_name = 'properties'  # Namespace for URL naming

urlpatterns = [
    # Authentication URLs
    path('', views.property_owner_signup, name='signup'),  # Default page: Signup
    
]
