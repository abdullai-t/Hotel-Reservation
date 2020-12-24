from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.conf.urls import url, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    url('admin/', admin.site.urls),
    url(r'^api/auth/', include('Accounts.API.urls')),
    url(r'^api/reservation/', include('Reservation.API.urls')),
    url(r'^api/news/', include('News.API.urls')),
]
urlpatterns+= static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()