from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views

from .views import home, terms

from customer.views import (
    dashboard,
    profile,
    upload_photo,
    deposit,
    withdraw,
    transfer,
    transactions,
    register,
)

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', home, name='home'),
    path('terms/', terms, name='terms'),

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
    path('profile/', profile, name='profile'),
    path('upload-photo/', upload_photo, name='upload_photo'),

    path('deposit/', deposit, name='deposit'),
    path('withdraw/', withdraw, name='withdraw'),
    path('transfer/', transfer, name='transfer'),
    path('transactions/', transactions, name='transactions'),
]

urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)