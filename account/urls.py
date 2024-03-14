
from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views

from . import views

app_name = "account"
urlpatterns = [
    path('login', auth_views.LoginView.as_view(next_page=reverse_lazy("forum:index")), name="login"),
    path('logout', auth_views.LogoutView.as_view(next_page=reverse_lazy("forum:index")),name="logout"),
    path('signup', views.signup, name="signup"),
    path('settings', views.settings, name="settings"),
    path('passwordchange', views.passwordchange, name="passwordchange"),
    path('deleteuser', views.deleteuser, name="deleteuser")
]