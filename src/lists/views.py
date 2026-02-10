<<<<<<< HEAD
from django.shortcuts import redirect, render
=======
from django.shortcuts import redirect, render, get_object_or_404
>>>>>>> origin/feature/completed-priority
from lists.models import Item, List

def home_page(request):
    return render(request, "home.html")

def view_list(request, list_id):
    our_list = List.objects.get(id=list_id)
    return render(request, "list.html", {"list": our_list})

def new_list(request):
    nulist = List.objects.create()
    Item.objects.create(
        text=request.POST["item_text"], 
        priority=request.POST["priority_text"], # เซฟลง Item
        list=nulist
    )
    return redirect(f"/lists/{nulist.id}/")

def add_item(request, list_id):
    our_list = List.objects.get(id=list_id)
    Item.objects.create(
        text=request.POST["item_text"], 
        priority=request.POST["priority_text"], # เซฟลง Item
        list=our_list
    )
    return redirect(f"/lists/{our_list.id}/")

<<<<<<< HEAD
=======
def edit_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    
    if request.method == 'POST':
        item.text = request.POST.get('item_text')
        item.priority = request.POST.get('priority')
        item.save()
        return redirect(f'/lists/{item.list.id}/')
    return render(request, 'edit_text.html', {'item': item})
>>>>>>> origin/feature/completed-priority
