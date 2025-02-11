from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as UserBaseAdmin
from .forms import UserCreationForm,UserChangeForm
from .models import User,OtpCode
from django.contrib.auth.models import Group

class UserAdmin(UserBaseAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('phone_number','email','is_active','is_admin')
    list_filter = ('email','is_active','is_admin')

    fieldsets = (
        ('Specification',{'fields':('phone_number','email','full_name','password')}),
        ('Permissions',{'fields':('is_active','is_admin','last_login','is_superuser','groups','user_permissions')})
    )

    add_fieldsets = (
        ('Specification',{'fields':('phone_number','email','full_name','password1','password2')}),
    )

    filter_horizontal = ('groups','user_permissions')
    ordering = ('is_admin','is_active')
    readonly_fields = ('last_login',)

    def get_form(self,request,obj=None,**kwargs):
        form = super().get_form(request,obj,**kwargs)
        is_superuser = request.user.is_superuser
        if not is_superuser:
            form.base_fields['is_superuser'].disabled = True
        return form

admin.site.register(OtpCode)
admin.site.register(User,UserAdmin)