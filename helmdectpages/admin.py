from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group

from helmdectpages.models import CustomUser, VideoConfig

class CustomUserAdminForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        exclude = ['user_permissions', 'groups','password','username']

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    readonly_fields = ('last_login', 'email', 'date_joined')
    form = CustomUserAdminForm
    # readonly_fields = ('id', )
    # list_display = ('email', 'firstname',
    #                 'middlename', 'lastname', 'mobile')
    # search_fields = ('email', 'firstname', 'middlename', 'lastname')

@admin.register(VideoConfig)
class VideoConfigAdmin(admin.ModelAdmin):
    pass

admin.site.site_header = 'Helmdetect Admin'  # Set your desired title here
admin.site.site_title = 'Helmdetect Admin'  # Set the title that appears on the browser tab
admin.site.index_title = 'Helmdetect Admin'  # Optional: Set the index title (appears above the authentication module)

admin.site.unregister((Group,))