from django.shortcuts import redirect, render, get_object_or_404
from lists.models import Item, List
from django.core.exceptions import ValidationError
from django.http import JsonResponse

def home_page(request):
    return render(request, "home.html")

def view_list(request, list_id):
    our_list = List.objects.get(id=list_id)
    error = None
    
    if request.method == "POST":
        item = Item(
            text=request.POST.get("item_text", ""), 
            priority=request.POST.get("priority_text", ""), 
            list=our_list
        )
        
        try:
            item.full_clean() # 1. Force model validation
            item.save()
            
            # 2. Return JSON if it's an AJAX request
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'id': item.id,
                    'text': item.text,
                    'priority': item.priority
                })
            return redirect(f"/lists/{our_list.id}/")
            
        except ValidationError:
            # 3. Catch the error and send it back as JSON with a 400 status
            error = "You can't have an empty list item"
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'error': error}, status=400)

    return render(request, "list.html", {"list": our_list, "error": error})
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

def edit_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    
    if request.method == 'POST':
        item.text = request.POST.get('item_text')
        item.priority = request.POST.get('priority')
        item.save()
        return redirect(f'/lists/{item.list.id}/')
    return render(request, 'edit_text.html', {'item': item})
