from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login as Login, logout as Logout

def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    else:
        return render(request, "users/user.html", {"username": request.user.username})

def login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username= username, password= password)
        if user is None:
            return render(request, "users/login.html", {"message": "Wrong credentials"})
        else:
            Login(request, user)
            return render(request, "users/user.html", {"username": username})


    return render(request, "users/login.html")

def logout(request):
    Logout(request)
    return render(request, "users/login.html", {"message": "Logged out"})