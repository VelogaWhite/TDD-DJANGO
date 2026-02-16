from django.shortcuts import redirect, render, get_object_or_404
from lists.models import Item, List

def home_page(request):
    return render(request, "home.html")

def view_list(request, list_id):
    our_list = List.objects.get(id=list_id)
    return render(request, "list.html", {"list": our_list})

def new_list(request):
    item_text = request.POST.get("item_text", "")
    priority_text = request.POST.get("priority_text", "")
    
    # Check if the input is empty
    if not item_text:
        return render(request, "home.html", {"error": "You can't have an empty list item"})
        
    nulist = List.objects.create()
    Item.objects.create(text=item_text, priority=priority_text, list=nulist)
    return redirect(f"/lists/{nulist.id}/")

def add_item(request, list_id):
    our_list = List.objects.get(id=list_id)
    item_text = request.POST.get("item_text", "")
    priority_text = request.POST.get("priority_text", "")
    
    # Check if the input is empty for existing lists too
    if not item_text:
        return render(request, "list.html", {"list": our_list, "error": "You can't have an empty list item"})
        
    Item.objects.create(text=item_text, priority=priority_text, list=our_list)
    return redirect(f"/lists/{our_list.id}/")

def edit_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    
    if request.method == 'POST':
        item.text = request.POST.get('item_text')
        item.priority = request.POST.get('priority')
        item.save()
        return redirect(f'/lists/{item.list.id}/')
    return render(request, 'edit_text.html', {'item': item})
