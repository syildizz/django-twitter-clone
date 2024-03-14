"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include, reverse_lazy
from django.views.generic import RedirectView
from django.views.defaults import page_not_found, server_error, permission_denied, bad_request

def custom_page_not_found(request):
    return page_not_found(request, None)

def custom_permission_denied(request):
    return permission_denied(request, None)

def custom_bad_request(request):
    return bad_request(request, None)


urlpatterns = [
    path('', RedirectView.as_view(url=reverse_lazy("forum:index"), permanent=True)),
    path('admin/', admin.site.urls),
    path('account/', include('account.urls'), name="account"),
    path('forum/', include('forum.urls'), name="forum"),
    path("404/", custom_page_not_found),
    path("500/", server_error),
    path("403/", custom_permission_denied),
    path("400/", custom_bad_request)
]
