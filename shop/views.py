from django.shortcuts import redirect, render
from shop.models import Category, Product
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

def dashboard(request):
    categories = Category.objects.all()
    data = {
        "categories": categories,
        }
    return render(request, "shop/index.html", context=data)

def detail(request):
    data = {
        "path": "Haqida"
    }
    return render(request, "shop/details.html", context=data)


def accounts(request):
    return render(request, "shop/accounts.html")


def cart(request):
    return render(request, "shop/cart.html")


def compare(request):
    return render(request, "shop/compare.html")


def login_register(request):
    return render(request, "shop/login-rehister.html")


def shop_page(request):
    products = Product.objects.all()
    # discount_prices = {}

    # for product in products:
    #     new_price = product.price - product.price*product.discount/100
    #     discount_prices[product.pk] = new_price 

    data = {
        "path": "Mahsulotlar",
        "products": products,
        # "discount_products": discount_prices
    }
    return render(request, "shop/shop.html", context=data)


def wishilst(request):
    return render(request, "shop/wishlist.html")

@login_required
def profile_user(request):
    data = {
        "path": "Profilm"
    }
    return render(request, "shop/accounts.html", context=data)


def login_user(request):
    data = {
        "path": "Login"
    }
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("dashboard")
    return render(request, "shop/login-register.html", context=data)

def logout_user(request):
    logout(request)
    return redirect("login_user")