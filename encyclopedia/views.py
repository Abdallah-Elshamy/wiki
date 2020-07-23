from django.shortcuts import render
from django import forms

from django.urls import reverse
from django.http import HttpResponseRedirect

from django.core.exceptions import ValidationError


from . import util

from markdown import markdown

from random import choice

def validate_entry_name(value):
    if value in util.list_entries():
        raise ValidationError(
            (f'{value} entry already exists')
        )

class CreateEntryForm(forms.Form):
    entry_name = forms.CharField(label="Title", validators=[validate_entry_name])
    entry_content = forms.CharField(widget=forms.Textarea, label="")

class EditEntryForm(forms.Form):
    entry_content = forms.CharField(widget=forms.Textarea, label="")

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entry_name):
    entry = util.get_entry(entry_name);
    if entry != None:
        return render(request, "encyclopedia/entry.html",{
            "entry": entry_name,
            "content": markdown(entry)
        })
    else:
        return render(request, "encyclopedia/notfound.html",{
            "entry": entry_name
        })

def search(request):
    if request.method == 'GET' and 'q' in request.GET:
        query = request.GET['q']
        entries = util.list_entries()
        if query in entries:
            return render(request, "encyclopedia/entry.html",{
                "entry": query,
                "content": markdown(util.get_entry(query))
            })
        else:
            query = query.lower()
            similar_entries = []
            for entry in entries:
                if query in entry.lower():
                    similar_entries.append(entry)
            return render(request, "encyclopedia/search_results.html",{
                "entries": similar_entries
            })
    return HttpResponseRedirect(reverse("index"))

def new(request):
    # Check if method is POST
    if request.method == "POST":
        # Take in the data the user submitted and save it as form
        form = CreateEntryForm(request.POST)
        # Check if form data is valid (server-side)
        if form.is_valid():
            # Isolate the task from the 'cleaned' version of form data
            entry_name = form.cleaned_data["entry_name"]
            entry_content = form.cleaned_data["entry_content"]
            # Add the new task to our list of tasks
            util.save_entry(entry_name, entry_content)
            # Redirect user to list of tasks
            return HttpResponseRedirect(reverse("entry", args=[entry_name]))
        else:
            # If the form is invalid, re-render the page with existing information.
            return render(request, "encyclopedia/new_entry.html", {
                "form": form
            })
    return render(request, "encyclopedia/new_entry.html", {
        "form": CreateEntryForm()
    })

def random(request):
    random_entry = choice(util.list_entries())
    return HttpResponseRedirect(reverse("entry", args=[random_entry]))

def edit(request, entry_name):
    # Check if method is POST
    if request.method == "POST":
        # Take in the data the user submitted and save it as form
        form = EditEntryForm(request.POST)
        # Check if form data is valid (server-side)
        if form.is_valid():
            # Isolate the task from the 'cleaned' version of form data
            entry_content = form.cleaned_data["entry_content"]
            # Add the new task to our list of tasks
            util.save_entry(entry_name, entry_content)
            # Redirect user to list of tasks
            return HttpResponseRedirect(reverse("entry", args=[entry_name]))
        else:
            # If the form is invalid, re-render the page with existing information.
            return render(request, "encyclopedia/edit_entry.html", {
                "entry_name": entry_name,
                "form": form
            })
    else:
        initial={'entry_content': util.get_entry(entry_name)}
        request.POST = {**initial, **request.POST}
        return render(request, "encyclopedia/edit_entry.html", {
            "entry_name": entry_name,
            "form": EditEntryForm(request.POST)
    })
