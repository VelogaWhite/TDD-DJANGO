from django.test import TestCase
from lists.models import Item, List
import lxml.html
from django.utils.html import escape

class HomePageTest(TestCase):
    def test_uses_home_template(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, "home.html")

    def test_renders_input_form(self):
        response = self.client.get("/")
        parsed = lxml.html.fromstring(response.content)  
        [form] = parsed.cssselect("form[method=POST]")   
        self.assertEqual(form.get("action"), "/lists/new")
        inputs = form.cssselect("input")  
        self.assertIn("item_text", [input.get("name") for input in inputs])
        self.assertIn("priority_text", [input.get("name") for input in inputs]) 

class NewListTest(TestCase):
    def test_can_save_a_POST_request(self):
        self.client.post('/lists/new', data={'item_text': 'A new list item'
                                             ,'priority_text': 'Medium'})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')
        self.assertEqual(new_item.priority, 'Medium')

    def test_redirects_after_POST(self):
        response = self.client.post('/lists/new', data={'item_text': 'A new list item'
                                                        ,'priority_text': 'Medium'})
        new_list = List.objects.first()
        self.assertRedirects(response, f'/lists/{new_list.id}/')

    def test_validation_errors_are_sent_back_to_home_page_template(self):
        # 1. จำลองการส่ง Form เปล่าๆ (POST request) ไปที่เซิร์ฟเวอร์
        response = self.client.post('/lists/new', data={'item_text': ''})
        
        # 2. เช็คว่าไม่มีอะไรถูกบันทึกลง Database
        self.assertEqual(Item.objects.count(), 0)
        
        # 3. เช็คว่าตอบกลับด้วยหน้าจอเดิม (home.html)
        self.assertTemplateUsed(response, 'home.html')
        
        # 4. เช็คว่ามีข้อความ Error แฝงมาใน HTML ที่ส่งกลับไปให้เบราว์เซอร์
        expected_error = escape("You can't have an empty list item")
        self.assertContains(response, expected_error)

    def test_invalid_list_items_arent_saved(self):
        # ลองส่งค่าว่างเข้าไป
        self.client.post("/lists/new", data={"item_text": ""})
        
        # เช็คว่าต้องไม่มี List หรือ Item โผล่มาใน Database เลย
        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)
        
class ListViewTest(TestCase):
    def test_uses_list_template(self):
        mylist = List.objects.create()
        response = self.client.get(f"/lists/{mylist.id}/")  
        self.assertTemplateUsed(response, "list.html")

    def test_renders_input_form(self):
        mylist = List.objects.create()
        response = self.client.get(f"/lists/{mylist.id}/")
        parsed = lxml.html.fromstring(response.content)
        [form] = parsed.cssselect("form[method=POST]")
        
        # Change this line to remove /add_item
        self.assertEqual(form.get("action"), f"/lists/{mylist.id}/") 
        
        inputs = form.cssselect("input")  
        self.assertIn("item_text", [input.get("name") for input in inputs])
        self.assertIn("priority_text", [input.get("name") for input in inputs])

    def test_displays_only_items_for_that_list(self):
        correct_list = List.objects.create()  
        Item.objects.create(text="itemey 1", priority="P1", list=correct_list)
        Item.objects.create(text="itemey 2", priority="P2", list=correct_list)

        other_list = List.objects.create()  
        Item.objects.create(text="other list item", priority="otherP", list=other_list)

        response = self.client.get(f"/lists/{correct_list.id}/")  

        self.assertContains(response, "itemey 1")
        self.assertContains(response, "P1")
        self.assertContains(response, "itemey 2")
        self.assertContains(response, "P2")
        self.assertNotContains(response, "other list item")  

    def test_can_save_a_POST_request_to_an_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(
            f"/lists/{correct_list.id}/",  
            # Add 'priority_text' so full_clean() doesn't reject it!
            data={
                "item_text": "A new item for an existing list",
                "priority_text": "High"
            },
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.get()
        self.assertEqual(new_item.text, "A new item for an existing list")
        self.assertEqual(new_item.priority, "High") # Optional: assert priority saved
        self.assertEqual(new_item.list, correct_list)

    def test_POST_redirects_to_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(
            f"/lists/{correct_list.id}/",  
            data={
                "item_text": "A new item for an existing list",
                "priority_text": "High"
            },
        )

        self.assertRedirects(response, f"/lists/{correct_list.id}/")

    def view_list(request, list_id):
        our_list = List.objects.get(id=list_id)
        error = None
        
        if request.method == "POST":
            # Safe initialization using .get() to prevent MultiValueDictKeyError
            item = Item(
                text=request.POST.get("item_text", ""), 
                priority=request.POST.get("priority_text", ""), 
                list=our_list
            )
            
            try:
                # Remove the duplicate item creation from here!
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
        