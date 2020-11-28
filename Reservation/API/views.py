from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from rest_framework.status import HTTP_400_BAD_REQUEST

from Accounts.models import User
from Reservation.API.serializers import RoomSerializer, ReservationSerializer
from Reservation.models import Room, Reservation


# ######################### Room requests ########################################################

# admin interactions
#  http://127.0.0.1:8000/api/reservation/create/room/
@api_view(['POST', ])
@authentication_classes([TokenAuthentication, ])
@permission_classes([IsAuthenticated])
def create_room(request):
    creator = User.objects.get(username=request.user)
    if not creator.is_manager:
        return Response({'error': 'You donot have the authorization to perform this task'}, status=HTTP_400_BAD_REQUEST)
    else:
        serializer = RoomSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            is_available = False if int(request.data["number_of_beds"]) < 1 else True
            serializer.save(is_available=is_available)
            data["success"] = "room successfully created"
        else:
            data["failure"] = "unable to create room please check the form"
        return Response(data=data)


# get all rooms
#  http://127.0.0.1:8000/api/reservation/rooms/
class get_rooms(ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ("name", "number_of_beds", "type", "bed_size", "cost", "is_available")


# edit room
#  http://127.0.0.1:8000/api/reservation/update/room/{name of room}/
@api_view(['PATCH'])
@authentication_classes([TokenAuthentication, ])
@permission_classes([IsAuthenticated])
def update_room_info(request, name):
    creator = User.objects.get(username=request.user)
    if not creator.is_manager:
        return Response({'error': 'You do not have the authorization to perform this task'},
                        status=HTTP_400_BAD_REQUEST)
    else:
        room = Room.objects.get(name=name)
        serializer = RoomSerializer(room, request.data, partial=True)
        data = {}
        if serializer.is_valid():
            serializer.save()
            is_available = False if room.number_of_beds < 1 else True
            serializer.save(is_available=is_available)
            data["data"] = serializer.data
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
    if not creator.is_manager:
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
# for the room pass the id of the room in  the request
# http://127.0.0.1:8000/api/reservation/add/reservation/
@api_view(['POST', ])
@authentication_classes([TokenAuthentication, ])
@permission_classes([IsAuthenticated])
def add_reservation(request):
    if request.method == "POST":
        guest = User.objects.get(username=request.user)
        room = Room.objects.get(pk=request.data["room"])
        serializer = ReservationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save(guest=guest, room=room)
            data["data"] = serializer.data
        else:
            data["failure"] = "unable to Add reservation please check the form"
        return Response(data)


# get all rooms
#  http://127.0.0.1:8000/api/reservation/rooms/
class get_reservations(ListAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ("check_in_date", "check_out_date", "cost", "room", "guest")


# deleting Room
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

    creator = User.objects.get(username=request.user)
    if reservation[0].guest == request.user or creator.is_manager == True:
        data = {}
        delete_operation = reservation.delete()
        if delete_operation:
            data["success"] = "room successfully deleted"
        else:
            data["failure"] = "unable to delete room"
        return Response(data=data)

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
        print(serializer.errors)
        serializer.save()
        data["success"] = "reservation successfully updated"
    else:
        data["failure"] = "we could not save this reservation info update"

    return Response(data)
