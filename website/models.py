from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token # Correct Token import

class Products(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock=models.IntegerField()
    def __str__(self):
        return self.name

class Reviews(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    user = models.CharField(max_length=100)
    rating = models.IntegerField()
    comment = models.TextField()
    def __str__(self):
        return f"Review by {self.user} for {self.product.name}"
    
class AuthUser(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    user_permissions = None  # Disable user permissions
    groups = None  # Disable groups
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    first_name = None
    last_name = None
    def __str__(self):
        return self.email

@receiver(post_save, sender=AuthUser) # Use the model class directly
def create_auth_user_token(sender, instance, created, **kwargs):
    if created:
        Token.objects.create(user=instance)