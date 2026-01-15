from django.shortcuts import redirect, render
from lists.models import Item, List, Priority

def home_page(request):
    return render(request, "home.html")

def view_list(request, list_id):
    our_list = List.objects.get(id=list_id)
    return render(request, "list.html", {"list": our_list})

def new_list(request):
    nulist = List.objects.create()
    nupriority = Priority.objects.create()
    Item.objects.create(text=request.POST["item_text"], list=nulist, priority=nupriority)
    return redirect(f"/lists/{nulist.id}/{nupriority.id}/")

def add_item(request, list_id, priority_id):
    our_list = List.objects.get(id=list_id)
    our_priority = Priority.objects.get(id=priority_id)
    Item.objects.create(text=request.POST["item_text"], list=our_priority, priority=our_priority)
    return redirect(f"/lists/{our_list.id}/{our_priority.id}/")