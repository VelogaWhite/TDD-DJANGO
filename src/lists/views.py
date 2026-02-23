from django.shortcuts import redirect, render, get_object_or_404
from lists.models import Item, List
from django.core.exceptions import ValidationError
from django.http import JsonResponse

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
    
    item = Item(text=item_text, priority=priority_text, list=our_list)
    
    # เช็คว่า Request นี้ส่งมาจาก JavaScript (Fetch API) หรือไม่
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.headers.get('Accept') == 'application/json'

    try:
        item.full_clean()
        item.save()
        
        # 2. ถ้าเป็น AJAX ให้ Return ข้อมูลเป็น JSON กลับไป
        if is_ajax:
            return JsonResponse({
                "id": item.id,
                "text": item.text,
                "priority": item.priority
            }, status=201)
            
    except ValidationError:
        error = "You can't have an empty list item"
        
        # 3. ถ้าเป็น AJAX ให้ Return Error กลับไปเป็น JSON
        if is_ajax:
            return JsonResponse({"error": error}, status=400)
            
        return render(request, "list.html", {"list": our_list, "error": error})
        
    return redirect(f"/lists/{our_list.id}/")

def edit_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    
    if request.method == 'POST':
        item.text = request.POST.get('item_text')
        item.priority = request.POST.get('priority')
        item.save()
        return redirect(f'/lists/{item.list.id}/')
    return render(request, 'edit_text.html', {'item': item})
