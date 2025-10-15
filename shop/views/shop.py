from django.shortcuts import render, get_object_or_404
from shop.models import Category, Product
from django.core.paginator import Paginator
from shop.views.cart import Cart


def dashboard(request):
    categories = Category.objects.all()
    cart = Cart(request)
    data = {
        "categories": categories,
        "cart_count": cart.get_quantity()
        }
    return render(request, "shop/index.html", context=data)

def detail(request):
    data = {
        "path": "Haqida"
    }
    return render(request, "shop/details.html", context=data)

def shop_page(request):
    products = Product.objects.all()
    paginator = Paginator(products, 2)
    cart = Cart(request)

    page = request.GET.get('page')

    page_products = paginator.get_page(page)

    data = {
        "path": "Mahsulotlar",
        "products": page_products,
        "cart_count": cart.get_quantity()
    }
    return render(request, "shop/shop.html", context=data)

def get_products_with_category(request, category_id):
    products = Product.objects.filter(category_id=category_id) 
    category = get_object_or_404(Category, id=category_id)

    data = {
        "path": category.name,
        "products": products,
    }
    return render(request, "shop/category_products.html", context=data)

