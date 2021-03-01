from django.contrib import admin

# Register your models here.

from .models import Airport, Flight, Passenger


class PassengerAdmin(admin.ModelAdmin):
    filter_horizontal = ("flights",)

admin.site.register(Airport)
admin.site.register(Flight)
admin.site.register(Passenger, PassengerAdmin)