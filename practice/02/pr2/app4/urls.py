from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name = "index"),
    path("merro", views.merro, name = "merro"),
    path("<str:ad>", views.isimli, name = "merro")
]