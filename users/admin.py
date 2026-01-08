from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'username', 'role', 'is_blocked', 'is_staff')
    list_filter = ('role', 'is_blocked')
    search_fields = ('email', 'username')
