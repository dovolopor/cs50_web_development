from django.db import models

# Create your models here.

class Airport(models.Model):
    code = models.CharField(max_length=3)
    city = models.CharField(max_length=64)

    def __str__(self):
      return f"{self.city} ({self.code})"


class Flight(models.Model):
    origin = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="departures")
    destination = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="arrivals")
    duration = models.IntegerField()

    def __str__(self):
      return f"{self.origin} to {self.destination}"

    def is_valid_flight(self):
      return self.destination != self.origin and self.duration > 0

class Passenger(models.Model):
    firstName = models.CharField(max_length=64)
    lastName = models.CharField(max_length=64)
    flights = models.ManyToManyField(Flight, blank=True, related_name="passengers")

    def is_valid_flight(self):
        return self.origin != self.destination or self.duration >= 0

    def __str__(self):
        return f"{self.firstName} {self.lastName}"
