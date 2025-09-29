"""
URL configuration for app project.

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
from django.urls import path, include
from django.shortcuts import redirect
from django.http import HttpResponse
import time

def hello_world(request):
    return HttpResponse("Hello World!")



urlpatterns = [
    path('admin/', admin.site.urls),
    path('contas/', include('apps.accounts.urls')),
    path('todolist/', include('apps.todolist.urls')),
    path('hello/', hello_world, name='hello_world'),
]

home_url = '/admin'
def custom_404_view(request, exception):
    if request.user.is_authenticated:
        return redirect(home_url)
    else:
        return redirect('login')

# Definir o handler404
handler404 = custom_404_view