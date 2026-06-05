from django.contrib import admin
from django.urls import path
from .views import home
from customer.views import dashboard, deposit

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('dashboard/', dashboard, name='dashboard'),
    path('deposit/', deposit, name='deposit'),
]