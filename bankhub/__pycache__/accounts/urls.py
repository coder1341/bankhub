from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views

from .views import home
from customer.views import (
    dashboard,
    deposit,
    withdraw,
    transfer,
    transactions,
    register
)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', home, name='home'),

    path('register/', register, name='register'),

    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name='login.html'
        ),
        name='login'
    ),

    path(
        'logout/',
        auth_views.LogoutView.as_view(),
        name='logout'
    ),

    path('dashboard/', dashboard, name='dashboard'),
    path('deposit/', deposit, name='deposit'),
    path('withdraw/', withdraw, name='withdraw'),
    path('transfer/', transfer, name='transfer'),
    path('transactions/', transactions, name='transactions'),
]