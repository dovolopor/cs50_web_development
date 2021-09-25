from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse

# Create your views here.

from .models import Flight, Passenger

def index(request):
    return render(request, "flights/index.html", { "flights": Flight.objects.all() })


def flight(request, flightId):
    try:
        flight = Flight.objects.get(id=flightId)
    except Flight.DoesNotExist:
        raise Http404("Flight not found.")
    
    print(flight)
    return render(request, "flights/flight.html", 
        { 
            "flight": flight, 
            "passengers": flight.passengers.all(),
            "non_passengers": Passenger.objects.exclude(flights = flight).all()
        })

def book(request, flightId):
    if request.method == "POST":
        flight = Flight.objects.get(pk=flightId)
        passenger= Passenger.objects.get(pk=int(request.POST["passenger"]))
        passenger.flights.add(flight)
        return HttpResponseRedirect(reverse("flight", args= (flightId,)))


        