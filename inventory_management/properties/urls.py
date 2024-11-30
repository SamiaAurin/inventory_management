from django.urls import path
from django.contrib.auth import views as auth_views  # For login and logout
from . import views

app_name = 'properties'  # Namespace for URL naming

urlpatterns = [
    # Authentication URLs
    path('', views.property_owner_signup, name='signup'),  # Default page: Signup
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Property-related URLs (protected)
    path('properties/', views.property_list, name='property_list'),
    path('properties/create/', views.property_create, name='property_create'),
    path('properties/<str:property_id>/', views.property_detail, name='property_detail'),
]
