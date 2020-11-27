from django.conf.urls import url
from Accounts.API.views import (guest_registration, manager_registration, PasswordRestView, passwordResetConfirmView,
                                passwordChangeView, profile, login_view)

app_name = 'Accounts'

urlpatterns = [
    url(r'^login/$', login_view, name="login"),
    url(r'^guest/$', guest_registration, name="register"),
    url(r'^manager/$', manager_registration, name="register"),
    url(r'^profile/$', profile, name="update_profile" ),
    #
    url(r'^password/reset/$', PasswordRestView, name="password_reset"),
    url(r'^reset/(?P<uidb64>[\w-]+)/(?P<token>[\w-]+)/$', passwordResetConfirmView, name="password_reset_confirm"),
    url(r'^password/change/$', passwordChangeView, name="password_change"),
    # url(r'^account/settings/$', user_profile_view, name="account_settings" ),

]