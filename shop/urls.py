from django.urls import path
from .views import dashboard, detail, accounts, cart, compare, login_register, shop_page, wishilst, profile_user, login_user, logout_user
from shop.views import shop_page

urlpatterns = [
    path('', dashboard, name="dashboard"),
    path('detail/', detail, name="detail"),
    path('accounts/', accounts, name="accounts"),
    path('cart/', cart, name="cart"),
    path('compare/', compare, name="compare"),
    path('login_register/', login_register, name="login_register"),
    path('shop/', shop_page, name="shop"),
    path('whishlist/', wishilst, name="whishilst"),
    path('profile/', profile_user, name="profile"),
    path('login/', login_user, name="login_user"),
    path('logout/', logout_user, name="logout_user"),
]