from django.contrib import admin
from shop.models import Category, Product

admin.site.register([Category, Product])

# Register your models here.
