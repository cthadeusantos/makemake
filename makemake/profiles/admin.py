from django.contrib import admin

from makemake.profiles.models import Profile

#@admin.register(Profile)
# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_username', 'id_number', )


admin.site.register(Profile, ProfileAdmin)