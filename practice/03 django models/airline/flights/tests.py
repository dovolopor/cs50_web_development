from django.db.models import Max
from django.test import TestCase
from django.test.client import Client

from .models import Flight, Passenger, Airport
# Create your tests here.


class FlightTest(TestCase):
    
    def setUp(self):
        # create airports
        airport1 = Airport.objects.create(code = "AAA", city = "city1")
        airport2 = Airport.objects.create(code = "BBB", city = "city2")

        # create flights
        flight1 = Flight.objects.create(origin= airport1, destination = airport2, duration = 100)
        flight2 = Flight.objects.create(origin= airport1, destination = airport1, duration = 100)
        flight3 = Flight.objects.create(origin= airport1, destination = airport2, duration = -100)

    def test_departures_count(self):
        airport1 = Airport.objects.get(code="AAA")
        self.assertEqual(airport1.departures.count(), 3)

    def test_arrivals_count(self):
        airport1 = Airport.objects.get(code="AAA")
        self.assertEqual(airport1.arrivals.count(), 1)

    def test_valid_flight(self):
        airport1 = Airport.objects.get(code="AAA")
        airport2 = Airport.objects.get(code="BBB")
        flight1 = Flight.objects.get(origin= airport1, destination = airport2, duration = 100)
        self.assertTrue(flight1.is_valid_flight())
        
    def test_invalid_flight_destination(self):
        a1 = Airport.objects.get(code="AAA")
        f = Flight.objects.get(origin=a1, destination=a1)
        self.assertFalse(f.is_valid_flight())

    def test_invalid_flight_duration(self):
        a1 = Airport.objects.get(code="AAA")
        a2 = Airport.objects.get(code="BBB")
        f = Flight.objects.get(origin=a1, destination=a2, duration=-100)
        self.assertFalse(f.is_valid_flight())

    def test_index(self):
        c = Client()
        response = c.get("/flights/")
        print(response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["flights"].count(), 3)
    
    def test_valid_flight_page(self):
        a1 = Airport.objects.get(code="AAA")
        f = Flight.objects.get(origin=a1, destination=a1)

        c = Client()
        response = c.get(f"/flights/{f.id}")
        self.assertEqual(response.status_code, 200)

    def test_invalid_flight_page(self):
        max_id = Flight.objects.all().aggregate(Max("id"))["id__max"]

        c = Client()
        response = c.get(f"/flights/{max_id + 1}")
        self.assertEqual(response.status_code, 404)

    def test_flight_page_passengers(self):
        f = Flight.objects.get(pk=1)
        p = Passenger.objects.create(firstName="Alice", lastName="Adams")
        f.passengers.add(p)

        c = Client()
        response = c.get(f"/flights/{f.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["passengers"].count(), 1)

    def test_flight_page_non_passengers(self):
        f = Flight.objects.get(pk=1)
        p = Passenger.objects.create(firstName="Alice", lastName="Adams")

        c = Client()
        response = c.get(f"/flights/{f.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["non_passengers"].count(), 1)





