from django.contrib import admin
from .models import CustomUser
from .forms import CustomUserCreationForm
from django.contrib.auth.admin import UserAdmin


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    add_form = CustomUserCreationForm
    list_display = ["username", "is_superuser", "is_staff", "last_login", "date_joined"]
    
    fieldsets = (
        *UserAdmin.fieldsets,
        (
            'Individuelle Daten',
            {
                'fields': (
                    'custom',
                    'phone',
                    'address'
                )
            }
        )
    )
