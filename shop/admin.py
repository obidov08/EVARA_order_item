from django.contrib import admin
from shop.models import Category, Product, Order, OrderItem

admin.site.register([Category, OrderItem, Order])

class ProductAdmin(admin.ModelAdmin):
    model = Product
    exclude = ("discount_price",)
    list_display = ("name", "price", "discount")
    list_display_links = ("name", "price", "discount")
    search_fields = ("name",)

admin.site.register(Product, ProductAdmin)  
