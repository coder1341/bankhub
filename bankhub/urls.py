from django.contrib import admin
from django.urls import path
from .views import home
from customer.views import dashboard, deposit, withdraw, transfer, transactions

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('dashboard/', dashboard, name='dashboard'),
    path('deposit/', deposit, name='deposit'),
    path('withdraw/', withdraw, name='withdraw'),
    path('transfer/', transfer, name='transfer'),
    path('transactions/', transactions, name='transactions'),
]