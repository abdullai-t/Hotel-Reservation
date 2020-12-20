from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from rest_framework.status import HTTP_400_BAD_REQUEST

from Accounts.API.serializers import ProfileSerializer
from Accounts.models import User, Profile
from Reservation.API.serializers import RoomSerializer, ReservationSerializer, ServiceSerializer, \
    UserServicesSerializer, BillSerializer, QueriesSerializer
from Reservation.models import Room, Reservation, Service, UserServices, Bill, Queries
import string
import random
from django.db.models import Sum
import requests


# http://127.0.0.1:8000/api/reservation/initial/
@api_view(['GET', ])
def initial(request):
    data = {}
    rooms = RoomSerializer(Room.objects.all(), many=True)
    services = ServiceSerializer(Service.objects.all(), many=True)
    data["rooms"] = rooms.data
    data["services"] = services.data
    return Response(data)


# ######################### Room requests ########################################################

# admin interactions
#  http://127.0.0.1:8000/api/reservation/create/room/
@api_view(['POST', ])
@authentication_classes([TokenAuthentication, ])
@permission_classes([IsAuthenticated])
def create_room(request):
    creator = User.objects.get(username=request.user)
    if not creator.is_staff:
        return Response({'error': 'You donot have the authorization to perform this task'}, status=HTTP_400_BAD_REQUEST)
    else:
        serializer = RoomSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data["success"] = "room successfully created"
        else:
            data["failure"] = "unable to create room please check the form"
        return Response(data=data)


# get all rooms
#  http://127.0.0.1:8000/api/reservation/rooms/
class get_rooms(ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ("name", "number_of_beds", "type", "bed_size", "cost", "is_available")


# edit room
#  http://127.0.0.1:8000/api/reservation/update/room/{name of room}/
@api_view(['PATCH'])
@authentication_classes([TokenAuthentication, ])
@permission_classes([IsAuthenticated])
def update_room_info(request, id):
    creator = User.objects.get(username=request.user)
    if not creator.is_manager:
        return Response({'error': 'You do not have the authorization to perform this task'},
                        status=HTTP_400_BAD_REQUEST)
    else:
        room = Room.objects.get(pk=id)
        serializer = RoomSerializer(room, request.data, partial=True)
        data = {}
        if serializer.is_valid():
            serializer.save()
            is_available = False if room.number_of_beds < 1 else True
            serializer.save(is_available=is_available)
            data["success"] = "room data succesfully updated"
        else:
            data["failure"] = "we could not save this rooms info update"

        return Response(data)


# deleting Room
# http://127.0.0.1:8000/api/reservation/delete/room/{name of room}/
@api_view(["DELETE", ])
@authentication_classes([TokenAuthentication, ])
@permission_classes([IsAuthenticated])
def delete_room(request, name):
    try:
        room = Room.objects.filter(name=name)
    except Room.DoesNotExist:
        return Response({'error': ' The room you want to delete does not exist'}, status=status.HTTP_404_NOT_FOUND)

    creator = User.objects.get(username=request.user)
    if not creator.is_manager or not creator.is_staff:
        return Response({'error': 'You do not have the authorization to perform this task'},
                        status=HTTP_400_BAD_REQUEST)
    else:
        data = {}
        delete_operation = room.delete()
        if delete_operation:
            data["success"] = "room successfully deleted"
        else:
            data["failure"] = "unable to delete room"
        return Response(data=data)


# ######################### Reservation requests ########################################################
# http://127.0.0.1:8000/api/reservation/add/reservation/
# @api_view(['POST', ])
# @authentication_classes([TokenAuthentication, ])
# @permission_classes([IsAuthenticated])
# def add_reservation(request):
#     if request.method == "POST":
#         guest = User.objects.get(username=request.user)
#         room = Room.objects.get(pk=request.data["room"])
#         serializer = ReservationSerializer(data=request.data)
#         data = {}
#         if serializer.is_valid():
#             serializer.save(guest=guest, room=room)
#             data["data"] = serializer.data
#         else:
#             data["failure"] = "unable to Add reservation please check the form"
#         return Response(data)


# get all reservations
#  http://127.0.0.1:8000/api/reservation/rooms/
class get_reservations(ListAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ("check_in_date", "check_out_date", "cost", "room", "guest")


# deleting a reservation
# http://127.0.0.1:8000/api/reservation/delete/reservation/id/
@api_view(["DELETE", ])
@authentication_classes([TokenAuthentication, ])
@permission_classes([IsAuthenticated])
def delete_reservation(request, id):
    try:
        reservation = Reservation.objects.filter(pk=id)
    except Reservation.DoesNotExist:
        return Response({'error': ' The Reservation you want to delete does not exist'},
                        status=status.HTTP_404_NOT_FOUND)
    data = {}
    delete_operation = reservation.delete()
    if delete_operation:
        data["success"] = "room successfully deleted"
    else:
        data["failure"] = "unable to delete room"
    return Response(data)


# update Reservation
# http://127.0.0.1:8000/api/reservation/update/reservation/id/
@api_view(["PATCH", ])
@authentication_classes([TokenAuthentication, ])
@permission_classes([IsAuthenticated])
def update_reservation(request, id):
    data = {}
    try:
        reservation = Reservation.objects.get(pk=id)
    except Reservation.DoesNotExist:
        return Response({'error': ' The Reservation you want to delete does not exist'},
                        status=status.HTTP_404_NOT_FOUND)
    serializer = ReservationSerializer(reservation, request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        data["success"] = "reservation successfully updated"
    else:
        data["failure"] = "we could not save this reservation info update"

    return Response(data)


# ######################### services requests ########################################################
# general services that are rendered by the hotel and created by only the admin
# http://127.0.0.1:8000/api/reservation/create/service/
@api_view(['POST', ])
@authentication_classes([TokenAuthentication, ])
@permission_classes([IsAuthenticated])
def create_service(request):
    creator = User.objects.get(username=request.user)
    if not creator.is_manager:
        return Response({'error': 'You donot have the authorization to perform this task'}, status=HTTP_400_BAD_REQUEST)
    else:
        serializer = ServiceSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data["success"] = "servive successfully created"
        else:
            data["failure"] = "unable to create service please check the form"
        return Response(data=data)


@api_view(["PATCH", ])
@authentication_classes([TokenAuthentication, ])
@permission_classes([IsAuthenticated])
def update_service(request, id):
    data = {}
    try:
        service = Service.objects.get(pk=id)
    except Service.DoesNotExist:
        return Response({'error': ' The Service you want to update does not exist'},
                        status=status.HTTP_404_NOT_FOUND)
    serializer = ServiceSerializer(service, request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        data["success"] = "Service successfully updated"
    else:
        data["failure"] = "we could not save this Service info update"

    return Response(data)


# get all servives
#  http://127.0.0.1:8000/api/reservation/services/
class get_services(ListAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ("service_name", "cost")


# http://127.0.0.1:8000/api/reservation/delete/service/{name of service}/
@api_view(["DELETE", ])
@authentication_classes([TokenAuthentication, ])
@permission_classes([IsAuthenticated])
def delete_service(request, name):
    try:
        service = Service.objects.filter(service_name=name)
    except Room.DoesNotExist:
        return Response({'error': ' The room you want to delete does not exist'}, status=status.HTTP_404_NOT_FOUND)

    creator = User.objects.get(username=request.user)
    if not creator.is_manager:
        return Response({'error': 'You do not have the authorization to perform this task'},
                        status=HTTP_400_BAD_REQUEST)
    else:
        data = {}
        delete_operation = service.delete()
        if delete_operation:
            data["success"] = "room successfully deleted"
        else:
            data["failure"] = "unable to delete room"
        return Response(data=data)


# delete user service
# http://127.0.0.1:8000/api/reservation/delete/user-service/{name of service}/
@api_view(["DELETE", ])
@authentication_classes([TokenAuthentication, ])
@permission_classes([IsAuthenticated])
def delete_user_service(request, name):
    try:
        user_service = UserServices.objects.filter(service__service_name=name, guest__username=request.user)
    except UserServices.DoesNotExist:
        return Response({'error': ' The service you want to delete does not exist'}, status=status.HTTP_404_NOT_FOUND)
    data = {}
    delete_operation = user_service.delete()
    if delete_operation:
        data["success"] = "service successfully deleted"
    else:
        data["failure"] = "unable to delete service"
    return Response(data=data)


# get all  user services
#  http://127.0.0.1:8000/api/reservation/user-services/
class get_user_service(ListAPIView):
    queryset = UserServices.objects.all()
    serializer_class = UserServicesSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)


# http://127.0.0.1:8000/api/reservation/specific/user-services/
@api_view(['GET', ])
@authentication_classes([TokenAuthentication, ])
@permission_classes([IsAuthenticated])
def get_specific_user_service(request):
    try:
        user_services = UserServices.objects.filter(guest__username=request.user)
    except UserServices.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = UserServicesSerializer(user_services, many=True)
    return Response(serializer.data)


# ######################### Bill requests ########################################################

# add
# get all and specif user
# delete
# --------------------------------- functions--------------------
def find_service(item):
    service = Service.objects.get(service_name=item)
    return (service)


def code_generator(size=5, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def sendEmail(res):
    msg_html = render_to_string('email/reservation_email.html',
                                {'fname': res.guest.fname.upper(), 'booking_code': res.booking_code,
                                 'full_name': res.guest.fname + " " + res.guest.lname,
                                 'check_in_date': res.check_in_date, 'check_out_date': res.check_out_date,
                                 "type": res.room.type, "hotel_address": "Cantoments, Accra",
                                 "site_name": "Luxcom Hotel",
                                 "hotel_number": "+233550751805"
                                 })
    send_mail(
        'Luxcom Hotel Reservation Notification',
        "",
        'luxcomh@gmail.com',
        [res.guest.email],
        html_message=msg_html,
    )


def sendSMS(res):
    msg = f"Hi {res.guest.fname}, Your reservation at Luxcom hotel has been successful. Your reservation code is {res.booking_code} with checkin date {res.check_in_date} and checkout date {res.check_out_date}. Thank you "
    payload = {"key": "d6fd93747a", "message": msg, "senderid": "Luxcom", "phone": res.guest.phone}
    url = "https://api.arispatbulk.com/sendmessage.php"
    requests.get(url, params=payload)


# some important functions

def send_generic_email(subject, msg, sender, receiver):
    email = EmailMessage(
        subject,
        msg,
        sender,
        [receiver,],
    )
    email.send()


def send_generic_sms(msg, receiver):
    payload = {"key": "d6fd93747a", "message": msg, "senderid": "Luxcom", "phone": receiver}
    url = "https://api.arispatbulk.com/sendmessage.php"
    requests.get(url, params=payload)


def add_reservation(reservation, user):
    guest = Profile.objects.get(user__username=user)
    room = Room.objects.get(pk=reservation["room"])
    serializer = ReservationSerializer(data=reservation)
    if serializer.is_valid():
        book_code = "LC" + code_generator()
        serializer.save(guest=guest, room=room, booking_code=book_code)
        reservation = Reservation.objects.get(room__pk=reservation["room"], guest__user__username=user,
                                              date=serializer.data["date"])
        sendEmail(reservation)
        sendSMS(reservation)
        return (reservation, reservation.id)


def add_user_service(services, user, reservation_id):
    guest = User.objects.get(username=user)
    reservation = Reservation.objects.get(pk=reservation_id)
    for x in services:
        UserServices.objects.get_or_create(guest=guest, reservation=reservation,
                                           service=find_service(x["service_name"]))
    services = UserServices.objects.filter(guest=user, reservation_id=reservation_id)
    return services


# --------------------------------------------------------------
@api_view(['POST', ])
@authentication_classes([TokenAuthentication, ])
@permission_classes([IsAuthenticated])
def bill(request):
    services = request.data["serviceObj"]
    reservation = request.data["reservationObj"]
    my_reservation, id = add_reservation(reservation, request.user)
    add_user_service(services, request.user, id)
    serializer = BillSerializer(data=request.data)
    data = {}
    if serializer.is_valid():
        serializer.save(reservation=my_reservation)
        data["reservationID"] = serializer.data["id"]
        return Response(data)

    else:
        print(serializer.errors)
        return Response({"Failure": "form invalid"})


class get_Bill(ListAPIView):
    queryset = Bill.objects.all()
    serializer_class = BillSerializer


@api_view(["PATCH", ])
@authentication_classes([TokenAuthentication, ])
@permission_classes([IsAuthenticated])
def update_bill(request, id):
    data = {}
    try:
        bill = Bill.objects.get(pk=id)
    except Bill.DoesNotExist:
        return Response({'error': ' The Bill you want to update does not exist'},
                        status=status.HTTP_404_NOT_FOUND)
    serializer = BillSerializer(bill, request.data, partial=True)
    if serializer.is_valid():
        paid = True if request.data.get("payment_mode") or bill.is_paid else False
        serializer.save(is_paid=paid)
        data["success"] = "bill successfully updated"
    else:
        data["failure"] = "we could not save this Service info update"
    return Response(data)


@api_view(["GET", ])
@authentication_classes([TokenAuthentication, ])
@permission_classes([IsAuthenticated])
def my_reservations(request):
    data = {}
    try:
        bill = Bill.objects.filter(reservation__guest__user__username=request.user)
    except Bill.DoesNotExist:
        return Response({'error': ' The Bill you want to update does not exist'},
                        status=status.HTTP_404_NOT_FOUND)
    serializer = BillSerializer(bill, many=True)
    data["reservations"] = serializer.data
    return Response(data)


@api_view(['GET', ])
def dashboard_view(request):
    guests_count = User.objects.filter(is_superuser=False, is_staff=False, is_manager=False).count()
    queries_count = Queries.objects.all().count()
    reservation_count = Bill.objects.all().count()
    services = ServiceSerializer(Service.objects.all(), many=True).data
    rooms = RoomSerializer(Room.objects.all(), many=True).data
    bills = BillSerializer(Bill.objects.all(), many=True).data
    staff = ProfileSerializer(Profile.objects.filter(user__is_staff=True, user__is_manager=True), many=True).data
    guests = ProfileSerializer(
        Profile.objects.filter(user__is_superuser=False, user__is_manager=False, user__is_staff=False), many=True).data
    earnings = Bill.objects.aggregate(Sum("total_cost"))
    queries = QueriesSerializer(Queries.objects.all(), many=True).data
    data = {}
    data['guests_count'] = guests_count
    data['queries_count'] =queries_count
    data['queries'] = queries
    data['reservation_count'] = reservation_count
    data['earnings'] = earnings['total_cost__sum']
    data['services'] = services
    data['staff'] = staff
    data['rooms'] = rooms
    data['bills'] = bills
    data['guests'] = guests

    return Response(data)


@api_view(['DELETE', ])
@authentication_classes([TokenAuthentication, ])
@permission_classes([IsAuthenticated])
def delete_all(request, table):
    data = {}
    if table == "RESERVATIONS":
        delete_operation = Reservation.objects.all().delete()
        if delete_operation:
            data["success"] = "successfully deleted"
        else:
            data["failure"] = "unable to delete"

    elif table == "ROOMS":
        delete_operation = Room.objects.all().delete()
        if delete_operation:
            data["success"] = "successfully deleted"
        else:
            data["failure"] = "unable to delete"

    elif table == "SERVICES":
        delete_operation = Service.objects.all().delete()
        if delete_operation:
            data["success"] = "successfully deleted"
        else:
            data["failure"] = "unable to delete"

    elif table == "QUERIES":
        delete_operation = Queries.objects.all().delete()
        if delete_operation:
            data["success"] = "successfully deleted"
        else:
            data["failure"] = "unable to delete"
    else:
        data["failure"] = "unable to delete because table does not exist "

    return  Response(data)


@api_view(['DELETE', ])
@authentication_classes([TokenAuthentication, ])
@permission_classes([IsAuthenticated])
def delete_query(request, id):
    try:
        query = Queries.objects.filter(pk=id)
    except Queries.DoesNotExist:
        return Response({'error': ' The Query you want to delete does not exist'}, status=status.HTTP_404_NOT_FOUND)
    data = {}
    delete_operation = query.delete()
    if delete_operation:
        data["success"] = "successfully deleted"
    else:
        data["failure"] = "unable to delete"
    return Response(data=data)


@api_view(['POST', ])
def add_queries(request):
    email = request.data.get("email")
    msg = request.data.get("message")
    subject = request.data.get("type")
    serializer = QueriesSerializer(data=request.data)
    data = {}
    if serializer.is_valid():
        serializer.save()
        data["success"] = "Message Successfully sent"
        send_generic_email(subject=subject, msg=msg, sender=email, receiver="luxcomh@gmail.com")
    else:
        data["failure"] = "Unable to send your message please check the form"
    return Response(data=data)


@api_view(['POST', ])
@authentication_classes([TokenAuthentication, ])
@permission_classes([IsAuthenticated])
def send_generic_message(request):
    msg_type = request.data.get("messageType")
    data = {}
    if msg_type == "EMAIL":
        email = request.data.get("receiver")
        msg = request.data.get("message")
        subject = request.data.get("subject")
        send_generic_email(subject=subject, msg=msg, sender="luxcomh@gmail.com", receiver=email)
        data["success"] = "email successfully sent"

    elif msg_type == "SMS":
        reciever = request.data.get("receiver")
        msg = request.data.get("message")
        send_generic_sms(msg=msg, receiver=reciever)
        data["success"]  = "sms successfully sent"
    else:
        print("hmmmmm")
    return  Response(data)