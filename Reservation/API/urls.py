from django.conf.urls import url
from Reservation.API.views import *

app_name = 'Reservation'

urlpatterns = [
    # POST REQUESTS
    url(r'^create/room/$', create_room, name="create_room"),
    # url(r'^add/reservation/$', add_reservation, name="add_reservation"),
    url(r'^create/service/$', create_service, name="create_service"),
    url(r'^chained/data/$', bill, name="bill"),
    url(r'^add/query/$', add_queries, name="add_queries"),
    url(r'^send/message/$', send_generic_message, name="send_generic_message"),

    # GET REQUESTS
    url(r'^rooms/$', get_rooms.as_view(), name="rooms"),
    url(r'^my/reservations/$', my_reservations, name="my_reservations"),
    # url(r'^bills/$', get_Bill.as_view(), name="bills"),
    url(r'^initial/$', initial, name="initial"),
    # url(r'^reservations/$', get_reservations.as_view(), name="get_reservations"),
    url(r'^dashboard/$', dashboard_view, name="dashboard_view"),
    url(r'^user-services/$', get_user_service.as_view(), name="get_user_service"),
    url(r'^specific/user-services/$', get_specific_user_service, name="get_specific_user_service"),

    # UPDATE REQUESTS
    url(r'^update/room/(?P<id>[\w\s-]+)/$', update_room_info, name="update_room_info"),
    url(r'^update/reservation/(?P<id>[\w-]+)/$', update_reservation, name="update_reservation"),
    url(r'^update/service/(?P<id>[\w\s-]+)/$', update_service, name="update_service"),
    url(r'^update/bill/(?P<id>[\w\s-]+)/$', update_bill, name="update_bill"),

    # DELETE REQUESTS
    url(r'^delete/room/(?P<name>[\w\s-]+)/$', delete_room, name="delete_room"),
    url(r'^delete/service/(?P<name>[\w\s-]+)/$', delete_service, name="delete_service"),
    url(r'^delete/reservation/(?P<id>[\w-]+)/$', delete_reservation, name="delete_reservation"),
    url(r'^delete/user-service/(?P<name>[\w\s-]+)/$', delete_user_service, name="delete_user_service"),
    url(r'^delete/table/(?P<table>[\w\s-]+)/$', delete_all, name="delete_all"),
    url(r'^delete/query/(?P<id>[\w-]+)/$', delete_query, name="delete_query"),

]