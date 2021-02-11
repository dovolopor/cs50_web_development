from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse



class NewTaskForm(forms.Form):
    taskName = forms.CharField(label="New Task") 
    priority = forms.IntegerField(label="priority", min_value=1, max_value=10)

tasks = ["itlik","serserilik", "atom mühendisliği"]
# Create your views here.
def index(request):
    if "tasks" not in request.session:
        request.session["tasks"] = []

    return render(request, "tasks/index.html", {"tasks": request.session["tasks"]})

def add(request):
    if request.method == 'POST':
        form = NewTaskForm(request.POST)
        if form.is_valid():
            taskName = form.cleaned_data["taskName"]
            request.session["tasks"] += [taskName]
            return HttpResponseRedirect(reverse("tasks:index"))
            
        else:
            return render(request, "tasks/add.html", {"form": form})
    
    return render(request, "tasks/add.html", {"form": NewTaskForm})