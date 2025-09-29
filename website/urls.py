from django.urls import path, include
from website import views

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('home/', views.home, name='home'),
    path('search/', views.search, name='search'),
    path('product/<int:pk>/', views.product_detail, name='product-detail'),
    path('cart/', views.cart, name='cart'),
    path('cart/update/', views.update_cart, name='update-cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('payment/', views.payment, name='payment'), # New URL for payment page
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('api/', include('website.api.urls')),
]