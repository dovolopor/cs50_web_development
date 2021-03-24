from django.urls import path

from . import views

app_name='encyclopedia'

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entName>", views.entry, name="entry"),
    path("new", views.new, name="new"),
    path("random", views.random, name="random"),
    path("edit/<str:entName>", views.edit, name="edit"),
    path("errorNew/<str:entName>", views.errorNew, name="errorNew"),
]
