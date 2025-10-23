from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from shop.forms import LoginForm, RegisterForm
from django.views.generic import View
from django.contrib import messages
from shop.models import Order
from shop.utils import Cart


class ProfileUserView(LoginRequiredMixin, View):
    def get(self, request):
        cart = Cart(request)

        orders = Order.objects.filter(user=request.user)
        orders_with_total = []
        for order in orders:
            orders_with_total.append({
                "order": order,
                "total": order.get_total()
            })

        data = {
            "path": "Profilm",
            "cart_count": cart.get_quantity(),
            "oders_with_total": orders_with_total
        }
        return render(request, "shop/accounts.html", context=data)

    def post(self, request):
            user = request.user
            first_name = request.POST.get()
            last_name = request.POST.get()

            if first_name and last_name:
                user.first_name = first_name
                user.last_name = last_name
                user.save()
                messages.success(request, "Profil ma'lumotlari yangilandi")

            messages.warning(request, "First name va Last name kiritilsin")
            return redirect("profile")

def accounts(request):
    return render(request, "shop/accounts.html")


def cart_(request):
    return render(request, "shop/cart.html")


def compare(request):
    return render(request, "shop/compare.html")


def login_register(request):
    return render(request, "shop/login-register.html")


def wishilst(request):
    return render(request, "shop/wishlist.html")


class ChangePasswordView(View):
    def post(self, request):
        old_password = request.POST.get("old_password")
        new_password = request.POST.get("new_password")
        repead_new_password = request.POST.get("repead_new_password")

        user = request.user
        if user.check_passowrd(old_password) and new_password==repead_new_password:
            user.set_password(new_password)
            user.save()
            print("To'g'ri")

        return redirect("dashboard")


class LoginUserView(View):
    def get(self, request):
        form = LoginForm()
        data = {
                    "path": "Login",
                    "form": form,
                }
        
        return render(request, "shop/login-register.html", context=data)


    def post(self, request):
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(request, username=username, password=password) 
            if user is not None:
                login(request, user)
                messages.success(request, "Siz muvoffaqqiyatli login qildingiz")
                return redirect("dashboard")
            
            messages.error(request, "Login yoki parol xato")
            
            data = {
                "path": "Login",
                "form": form,
                "error": "Foydalanuvchi nomi yoki paroli xato!"
            }
            return render(request, "shop/login-register.html", context=data)
        
        data = {
                    "path": "Login",
                    "form": form,
                    "error": "Formani to'g'ri to'ldiring."
        }
        return render(request, "shop/login-register.html", context=data)

        
def logout_user(request):
    logout(request)
    messages.success(request, "Siz tizimdan chiqdingiz!")
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
