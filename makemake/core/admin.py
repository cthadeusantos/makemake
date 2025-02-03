from django.contrib import admin
from makemake.core.models import UserLog

@admin.register(UserLog)
class UserLogAdmin(admin.ModelAdmin):
    list_display = ("user", "login_time", "last_login_ip")
    search_fields = ("user__username", "last_login_ip")
