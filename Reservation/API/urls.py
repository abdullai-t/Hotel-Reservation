from django.conf.urls import url
from Reservation.API.views import *

app_name = 'Reservation'

urlpatterns = [
    # POST REQUESTS
    url(r'^create/room/$', create_room, name="create_room"),
    # url(r'^add/reservation/$', add_reservation, name="add_reservation"),
    url(r'^create/service/$', create_service, name="create_service"),
    url(r'^chained/data/$', bill, name="bill"),

    # GET REQUESTS
    url(r'^rooms/$', get_rooms.as_view(), name="rooms"),
    url(r'^initial/$', initial, name="initial"),
    url(r'^reservations/$', get_reservations.as_view(), name="get_reservations"),
    url(r'^services/$', get_services.as_view(), name="get_services"),
    url(r'^user-services/$', get_user_service.as_view(), name="get_user_service"),
    url(r'^specific/user-services/$', get_specific_user_service, name="get_specific_user_service"),

    # UPDATE REQUESTS
    url(r'^update/room/(?P<name>[\w\s-]+)/$', update_room_info, name="update_room_info"),
    url(r'^update/reservation/(?P<id>[\w-]+)/$', update_reservation, name="update_reservation"),
    url(r'^update/service/(?P<name>[\w\s-]+)/$', update_service, name="update_service"),

    # DELETE REQUESTS
    url(r'^delete/room/(?P<name>[\w\s-]+)/$', delete_room, name="delete_room"),
    url(r'^delete/service/(?P<name>[\w\s-]+)/$', delete_service, name="delete_service"),
    url(r'^delete/reservation/(?P<id>[\w-]+)/$', delete_reservation, name="delete_reservation"),
    url(r'^delete/user-service/(?P<name>[\w\s-]+)/$', delete_user_service, name="delete_user_service"),

]