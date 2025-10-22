from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'team_number', 'assigned_at')
    list_filter = ('team_number', 'assigned_at')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('assigned_at',)
