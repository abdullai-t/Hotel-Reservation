from django.conf.urls import url
from Reservation.API.views import *

app_name = 'Reservation'

urlpatterns = [
    # POST REQUESTS
    url(r'^create/room/$', create_room, name="create_room"),
    url(r'^add/reservation/$', add_reservation, name="add_reservation"),

    # GET REQUESTS
    url(r'^rooms/$', get_rooms.as_view(), name="rooms"),
    url(r'^reservations/$', get_reservations.as_view(), name="get_reservations"),

    # UPDATE REQUESTS
    url(r'^update/room/(?P<name>[\w\s-]+)/$', update_room_info, name="update_room_info"),
    url(r'^update/reservation/(?P<id>[\w-]+)/$', update_reservation, name="update_reservation"),

    # DELETE REQUESTS
    url(r'^delete/room/(?P<name>[\w\s-]+)/$', delete_room, name="delete_room"),
    url(r'^delete/reservation/(?P<id>[\w-]+)/$', delete_reservation, name="delete_reservation"),

]