from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# Register your models here.

#admin.site.register(User, UserAdmin)

@admin.register(User)
class UserManager(admin.ModelAdmin):
    list_display = ('username', 'profile_name', 'is_active', 'is_staff', 'is_superuser', 'date_joined', 'last_login')
    list_filter = ('is_active', 'is_staff', 'is_superuser', 'date_joined', 'last_login')
    fields = [('username', 'profile_name'), 'password', ('bio', 'email'), ('is_active', 'is_staff', 'is_superuser'), ('date_joined', 'last_login'), ('first_name', 'last_name')]
