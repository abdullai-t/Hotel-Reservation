from rest_framework import serializers
from Reservation.models import Room, Reservation, Bill, Service


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ["id","name", "number_of_beds", "type", "bed_size", "cost", "is_available"]


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ["service_name", "cost", "is_paid", "guest"]


class ReservationSerializer(serializers.ModelSerializer):
    room = RoomSerializer(read_only=True)
    class Meta:
        model = Reservation
        fields = ["id","date", "check_in_date", "check_out_date", "number_of_adult", "number_of_children", "cost", "room",
                  "guest"]


class BillSerializer(serializers.ModelSerializer):
    service = ServiceSerializer(read_only=True)
    reservation = ReservationSerializer(read_only=True)

    class Meta:
        model = Bill
        fields = ["total_cost", "is_paid", "payment_mode", "reservation", "staff", "service"]