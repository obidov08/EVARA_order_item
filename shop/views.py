from django.shortcuts import render
from shop.models import Category, Product

def dashboard(request):
    categories = Category.objects.all()
    produtcs = Product.objects.all()
    data = {
        "categories": categories,
        "produtcs":produtcs
        }
    return render(request, "shop/index.html", context=data)

def detail(request):
    return render(request, "shop/details.html")


def accounts(request):
    return render(request, "shop/accounts.html")


def cart(request):
    return render(request, "shop/cart.html")


def checkout(request):
    return render(request, "shop/checkout.html")


def compare(request):
    return render(request, "shop/compare.html")


def login(request):
    return render(request, "shop/login-register.html")


def shop(request):
    return render(request, "shop/shop.html")


def wishilst(request):
    return render(request, "shop/wishlist.html")