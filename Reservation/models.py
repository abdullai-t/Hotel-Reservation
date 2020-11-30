from django.db import models

from Accounts.models import User


class Room(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    number_of_beds = models.IntegerField(null=False, blank=False)
    type = models.CharField(max_length=50, null=False, blank=False)
    bed_size = models.CharField(max_length=50, null=False, blank=False)
    cost = models.IntegerField(null=False, blank=False)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Service(models.Model):
    service_name = models.CharField(max_length=50, null=False, blank=False)
    cost = models.DecimalField(decimal_places=2, max_digits=10)

    def __str__(self):
        return self.service_name


class UserServices(models.Model):
    guest = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, blank=True, null=True)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return self.guest.username


class Reservation(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    number_of_adult = models.IntegerField(null=False, blank=False)
    number_of_children = models.IntegerField(null=False, blank=False)
    cost = models.IntegerField(null=False, blank=False)
    room = models.OneToOneField(Room, on_delete=models.CASCADE, blank=True, null=True)
    guest = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.guest.username


class Bill(models.Model):
    total_cost = models.DecimalField(decimal_places=2, max_digits=10)
    is_paid = models.BooleanField(default=False)
    payment_mode = models.CharField(max_length=20, null=False, blank=False)
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE, blank=True, null=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, blank=True, null=True)
    staff = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.reservation.guest.username
