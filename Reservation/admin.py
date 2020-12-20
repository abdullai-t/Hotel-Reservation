from django.contrib import admin

# Register your models here.
from Reservation.models import Room, Service, Bill, Reservation, UserServices, Queries

admin.site.register(Room)
admin.site.register(Service)
admin.site.register(UserServices)
admin.site.register(Bill)
admin.site.register(Reservation)
admin.site.register(Queries)