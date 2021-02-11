from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return render(request, "app4/index.html")


def merro(request):
    return HttpResponse("Merro")


def isimli(request, ad):
    return render(request, "app4/isimli.html", {"isim" : ad})
    