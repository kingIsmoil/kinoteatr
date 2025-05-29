from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Review

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'phone_number', 'age', 'is_active', 'is_staff')
    search_fields = ('username', 'email', 'phone_number')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('email', 'phone_number', 'age')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'phone_number', 'age', 'password1', 'password2'),
        }),
    )

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'star_number', 'movie_id', 'is_active', 'created_at')
    list_filter = ('is_active', 'star_number')
    search_fields = ('user__username', 'description')

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Review, ReviewAdmin)