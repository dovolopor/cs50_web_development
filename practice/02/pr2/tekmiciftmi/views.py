from django.shortcuts import render
import random;
# Create your views here.

def index(request):
    return render(request, "tekmiciftmi/index.html", {"tek": random.random() < 0.5})