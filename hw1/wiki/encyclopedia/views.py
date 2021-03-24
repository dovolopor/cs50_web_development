from django.shortcuts import render
from markdown2 import Markdown
from . import util
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms
from random import randrange

mardowner = Markdown()

def index(request):
    querry = request.GET.get('q', None)
    if querry == None:
        return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
        
    })
    else:
        return saerch(request, querry)

def entry(request, entName, content = None):
    if request.method == 'POST': # comes from edit page
        form = EditEntryForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data["content"]
            util.save_entry(entName, bytes(content, "utf8"))
            print(content)
        else:
            return render(request, "encyclopedia/edit.html", {"form": form, 'entName': entName})

    if content == None:
        content = util.get_entry(entName)
    return render(request, "encyclopedia/entry.html", {
        "title": entName.capitalize(),
        "content": mardowner.convert(content)
    })

def saerch(request, entName):
    content = util.get_entry(entName)
    allEntries = util.list_entries()
    entName = entName.lower()
    if content == None:
        return render(request, "encyclopedia/searchResult.html", {
        "entries": [s for s in allEntries if entName in s.lower()]
        })
    else:
        return entry(request, entName)

class NewAddForm(forms.Form):
    entName = forms.CharField(label="Title", min_length=1) 
    content = forms.CharField(widget=forms.Textarea, min_length=10)

def new(request):
    if request.method == 'POST':
        form = NewAddForm(request.POST)
        if form.is_valid():
            entName = form.cleaned_data["entName"]
            content = form.cleaned_data["content"]
            if util.get_entry(entName) == None:
                util.save_entry(entName, bytes(content, "utf8"))
                return entry(request, entName)
            else:
                return HttpResponseRedirect(reverse("encyclopedia:errorNew", kwargs={"entName" : entName}))
        else:
            return render(request, "encyclopedia/new.html", {"form": form})
    
    return render(request, "encyclopedia/new.html", {"form": NewAddForm})

def errorNew(request, entName):
    return render(request, "encyclopedia/newError.html", {"entName": entName})

class EditEntryForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea, min_length=10)

def edit(request, entName):
    print("Edit:")
    print(util.get_entry(entName))
    return render(request, "encyclopedia/edit.html", {"entName": entName, "form": EditEntryForm(initial={"content" : util.get_entry(entName)})})

def random(request):
    allEntries = util.list_entries()
    selectedEntry = allEntries[randrange(0, len(allEntries))]
    return entry(request, selectedEntry)
    
    
