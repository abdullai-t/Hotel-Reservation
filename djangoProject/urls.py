
from django.contrib import admin
from django.conf.urls import url, include

urlpatterns = [
    url('admin/', admin.site.urls),
    url(r'^api/auth/', include('Accounts.API.urls')),
    url(r'^api/reservation/', include('Reservation.API.urls')),
]
