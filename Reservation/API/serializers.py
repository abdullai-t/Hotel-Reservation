from rest_framework import serializers
from Reservation.models import Room, Reservation, Bill, Service, UserServices


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ["id","name", "number_of_beds", "type", "bed_size", "cost", "is_available","image"]


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ["id","service_name", "cost"]

class UserServicesSerializer(serializers.ModelSerializer):
    service = ServiceSerializer(read_only=True)
    class Meta:
        model = UserServices
        fields = ["id","service", "guest", "reservation"]

class ReservationSerializer(serializers.ModelSerializer):
    room = RoomSerializer(read_only=True)
    class Meta:
        model = Reservation
        fields = ["id","date", "check_in_date", "check_out_date", "number_of_adult", "number_of_children", "cost", "room",
                  "guest"]


class BillSerializer(serializers.ModelSerializer):
    reservation = ReservationSerializer(read_only=True)

    class Meta:
        model = Bill
        fields = ["id","total_cost", "is_paid", "payment_mode", "reservation"]
