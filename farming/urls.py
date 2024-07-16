"""
URL configuration for farming project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from app.views import *

from allauth.account.views import *
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path("accounts/",include("allauth.urls")),
    path("logout/",signout),
    path('',home),
    path('dashboard/',dashboard),
    path('soil/',recommend),
    path('farm/<str:crop>/',farm),
    path('productions/',productions),
    path('productions/update/<id>/<value>/',update_productions),
    path('rbi/',rbi),
    path('crops/',crops),
    path('products/',products),
    path('myproducts/',my_products),
    path('editproducts/<id>/',edit_products),
    path('deleteproducts/<id>/',delete_products),
    path('products/buy/<str:crop>/',buy_products),
    path('products/sell/<str:crop>/',sell_products),
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
