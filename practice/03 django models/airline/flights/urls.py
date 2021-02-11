from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:flightId>", views.flight, name="flight"),
    path("<int:flightId>/book", views.book, name="book")
]