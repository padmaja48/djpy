from django.urls import path
from website.api import views
from rest_framework.authtoken import views as drf_views
urlpatterns = [
    # Product API
    path('token/',drf_views.obtain_auth_token, name='api-token-auth'),
    path('products/', views.product_list, name='api-product-list'),
    path('products/create/', views.product_create, name='api-product-create'),
    path('products/update/<int:pk>/', views.product_update, name='api-product-update'),
    path('products/delete/<int:pk>/', views.product_delete, name='api-product-delete'),
    
]