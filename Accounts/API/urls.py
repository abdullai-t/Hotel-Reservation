from django.conf.urls import url
from Accounts.API.views import (guest_registration, manager_registration, PasswordRestView, passwordResetConfirmView,
                                passwordChangeView, profile, login_view,admin_login,delete_staff)

app_name = 'Accounts'

urlpatterns = [
    url(r'^login/$', login_view, name="login"),
    url(r'admin-login/$', admin_login, name="admin_login"),
    url(r'^guest/$', guest_registration, name="register"),
    url(r'^staff/$', manager_registration, name="register"),
    url(r'^profile/$', profile, name="update_profile" ),
    #
    url(r'^password/reset/$', PasswordRestView, name="password_reset"),
    url(r'^reset/(?P<uidb64>[\w-]+)/(?P<token>[\w-]+)/$', passwordResetConfirmView, name="password_reset_confirm"),
    url(r'^password/change/$', passwordChangeView, name="password_change"),
    url(r'^delete/staff/(?P<email>[\w-]+)/$', delete_staff, name="delete_staff"),
]