from django.contrib import admin
from .models import User, Staff
from django.contrib.auth.admin import UserAdmin


class AccountAdmin(UserAdmin):
    list_display = ('email', 'username', 'date_joined', 'last_login', 'is_admin', 'is_staff', 'is_manager',"is_accountant", "fname", "lname", "isBlackListed", "phone", "nationality", "homeAddress")
    search_fields = ('email', 'username',)
    readonly_fields = ('date_joined', 'last_login')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


# Register your models here.

admin.site.register(User, AccountAdmin)
admin.site.register(Staff)
