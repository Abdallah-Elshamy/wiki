from django.shortcuts import render

from . import util

from markdown import markdown


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
    
