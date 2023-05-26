from django.contrib import admin
from .models import *
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import CustomUserCreationForm


class CustomUserAdmin(BaseUserAdmin):
    add_form = CustomUserCreationForm

    # Customize the fields displayed in the user change form in the Django admin
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email', 'phone_number', 'address')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )

    # Customize the fields displayed in the user creation form in the Django admin
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'first_name', 'last_name', 'email', 'phone_number', 'address'),
        }),
    )

admin.site.register(Customer, CustomUserAdmin)

admin.site.register(Item)
admin.site.register(Profile)
admin.site.register(Cart)
admin.site.register(Order)