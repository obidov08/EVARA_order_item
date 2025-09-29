from django.urls import path
from .views import dashboard, detail, accounts

urlpatterns = [
    path('', dashboard, name="dashboard"),
    path('detail/', detail, name="detail"),
    path('accounts/', accounts, name="accounts")
]