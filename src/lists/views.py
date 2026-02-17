from django.shortcuts import redirect, render, get_object_or_404
from lists.models import Item, List
from django.core.exceptions import ValidationError

def home_page(request):
    return render(request, "home.html")

def view_list(request, list_id):
    our_list = List.objects.get(id=list_id)
    return render(request, "list.html", {"list": our_list})

def new_list(request):
    nulist = List.objects.create()
    item_text = request.POST.get("item_text", "")
    priority_text = request.POST.get("priority_text", "")
    
    # 1. สร้าง Item ขึ้นมา แต่ยังไม่เซฟ
    item = Item(text=item_text, priority=priority_text, list=nulist)
    
    try:
        # 2. ให้ Model เป็นคนตรวจ! ถ้า text ว่าง มันจะพ่น ValidationError ออกมา
        item.full_clean() 
        item.save()
    except ValidationError:
        # 3. ถ้าเกิด Error แปลว่าข้อมูลไม่ผ่านเกณฑ์
        nulist.delete() # ลบ List ขยะทิ้ง
        return render(request, "home.html", {"error": "You can't have an empty list item"})
        
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
