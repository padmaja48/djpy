from django.contrib import admin
from website.models import Products, Reviews, AuthUser

# Register your models here.
admin.site.register(Products)
admin.site.register(Reviews)
admin.site.register(AuthUser)