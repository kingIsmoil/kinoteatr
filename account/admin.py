from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Review

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'phone_number', 'age', 'is_active', 'date_joined')
    search_fields = ('username', 'email', 'phone_number')
    list_filter = ('is_active', 'is_staff', 'date_joined')
    ordering = ('-date_joined',)
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'phone_number', 'age')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'phone_number', 'age', 'password1', 'password2'),
        }),
    )

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'movie_id', 'star_number', 'is_active', 'created_at')
    list_filter = ('is_active', 'star_number', 'created_at')
    search_fields = ('user__username', 'description', 'movie_id')
    ordering = ('-created_at',)
    raw_id_fields = ('user',)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Review, ReviewAdmin)