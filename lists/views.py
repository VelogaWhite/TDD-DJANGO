from django.shortcuts import redirect, render
from lists.models import Item, List, Priority

def home_page(request):
    return render(request, "home.html")

def view_list(request, list_id):
    our_list = List.objects.get(id=list_id)
    items = our_list.item_set.all()
    priorities = our_list.priority_set.all()
    items_and_priorities = zip(items, priorities)
    
    return render(request, "list.html", {
        "list": our_list, 
        "items_and_priorities": items_and_priorities
    })

def new_list(request):
    nulist = List.objects.create()
    Item.objects.create(text=request.POST["item_text"], list=nulist)
    Priority.objects.create(text=request.POST["priority_text"], list=nulist)
    return redirect(f"/lists/{nulist.id}/")

def add_item(request, list_id):
    our_list = List.objects.get(id=list_id)
    Item.objects.create(text=request.POST['item_text'], list=our_list)
    priority_text = request.POST.get('priority_text', '')
    Priority.objects.create(text=priority_text, list=our_list)
    return redirect(f'/lists/{our_list.id}/')

def add_priority(request, list_id):
    our_list = List.objects.get(id=list_id)
    Priority.objects.create(text=request.POST["priority_text"], list=our_list)
    return redirect(f"/lists/{our_list.id}/")