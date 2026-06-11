# accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from .models import CustomUser , Profile
# from django.contrib.auth import get_user_model
# CustomUser = get_user_model()

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    search_fields = ("email",)
    list_display = ('email', 'is_staff', 'type')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('type',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser','groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'created_date', 'updated_date')}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2", "type"),
            },
        ),
    )
    readonly_fields = ('created_date', 'updated_date')
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions',)

# class ProfileAdmin(UserAdmin):
#     model = Profile
#     list_display = ("user","first_name","last_name","phone_number")
#     search_fields = ("user",)

class ProfileAdmin(admin.ModelAdmin):
    model = Profile
    list_display = ("user","first_name","last_name","phone_number")
    search_fields = ("user",)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Profile,ProfileAdmin)