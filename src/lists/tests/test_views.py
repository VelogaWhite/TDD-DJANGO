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
  
class NewItemTest(TestCase):
    def test_can_save_a_POST_request_to_an_existing_list(self):
        correct_list = List.objects.create()

        self.client.post(
            f"/lists/{correct_list.id}/add_item",
            data={"item_text": "A new item for an existing list",
                  "priority_text": "High"
            },
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.get()
        self.assertEqual(new_item.text, "A new item for an existing list")
        self.assertEqual(new_item.priority, "High")
        self.assertEqual(new_item.list, correct_list)

    def test_redirects_to_list_view(self):
        correct_list = List.objects.create()

        response = self.client.post(
            f"/lists/{correct_list.id}/add_item",
            data={"item_text": "A new item for an existing list",
                  "priority_text": "Low"},
        )

        self.assertRedirects(response, f"/lists/{correct_list.id}/")

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
        self.assertEqual(form.get("action"), f"/lists/{mylist.id}/add_item")
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
