from django.shortcuts import render, redirect, get_object_or_404
from shop.models import Category, Product
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .forms import LoginForm, RegisterForm

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
    return render(request, "shop/login-register.html")


def shop_page(request):
    products = Product.objects.all()
    paginator = Paginator(products, 2)

    page = request.GET.get('page')

    page_products = paginator.get_page(page)

    data = {
        "path": "Mahsulotlar",
        "products": page_products,
    }
    return render(request, "shop/shop.html", context=data)

def category_products_with_id(request, category_id):
    products = Product.objects.filter(category_id=category_id) 
    category = get_object_or_404(Category, id=category_id)

    data = {
        "path": category.name,
        "products": products,
    }
    return render(request, "shop/category_products.html", context=data)

def wishilst(request):
    return render(request, "shop/wishlist.html")

@login_required
def profile_user(request):
    data = {
        "path": "Profilm"
    }
    return render(request, "shop/accounts.html", context=data)


def login_user(request):

    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(request, username=username, password=password) 
            if user is not None:
                login(request, user)
                return redirect("dashboard")
        
        else:
            data = {
                "path": "Login",
                "form": form,
            }
            return render(request, "shop/login-register.html", context=data)
        
    form = LoginForm()

    data = {
                "path": "Login",
                "form": form,
            }
    
    return render(request, "shop/login-register.html", context=data)

        
def logout_user(request):
    logout(request)
    return redirect("dashboard")


def register_user(request):

    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')

            user = User(first_name=first_name, last_name=last_name, username=username, email=email)
            user.set_password(password)

            user.save()
            return redirect('login_user')
        else:
            data = {
            "path": "Register",
            "form": form
        }
        return render(request, "shop/register.html", context=data) 


    form = RegisterForm()
    data = {
        "path": "Register",
        "form": form,
    }
    return render(request, "shop/register.html", context=data)
