from django.test import TestCase
from lists.models import Item, List

class HomePageTest(TestCase):
    def test_uses_home_template(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, "home.html")

    def test_renders_input_form(self):
        response = self.client.get("/")
        self.assertContains(response, '<form method="POST" action="/lists/new">')
        self.assertContains(
            response,
            '<input name="item_text" id="id_new_item" placeholder="Enter a to-do item" />',
            html=True,
        )
        self.assertContains(
            response,
            '<input name="priority_text" id="id_new_priority" placeholder="Enter a to-do priority" />',
            html=True,
        )

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

class ListViewTest(TestCase):
    def test_uses_list_template(self):
        mylist = List.objects.create()
        response = self.client.get(f"/lists/{mylist.id}/")  
        self.assertTemplateUsed(response, "list.html")

    def test_renders_input_form(self):
        mylist = List.objects.create()
        response = self.client.get(f"/lists/{mylist.id}/")
        self.assertContains(
            response,
            f'<form method="POST" action="/lists/{mylist.id}/add_item">',
        )
        self.assertContains(
            response,
            '<input name="item_text" id="id_new_item" placeholder="Enter a to-do item" />',
            html=True,
        )
        self.assertContains(
            response,
            '<input name="priority_text" id="id_new_priority" placeholder="Enter a to-do priority" />',
            html=True,
        )


    def test_displays_only_items_for_that_list(self):
        correct_list = List.objects.create()  
        Item.objects.create(text="itemey 1", priority="P1", list=correct_list)
        Item.objects.create(text="itemey 2", priority="P2", list=correct_list)

        other_list = List.objects.create()  
        Item.objects.create(text="other list item", priority="otherP", list=other_list)

        response = self.client.get(f"/lists/{correct_list.id}/")  

        self.assertContains(response, "itemey 1")
        self.assertContains(response, "(P1)")
        self.assertContains(response, "itemey 2")
        self.assertContains(response, "(P2)")
        self.assertNotContains(response, "other list item")  

class ListAndItemModelsTest(TestCase):
    def test_saving_and_retrieving_items(self):
        mylist = List()
        mylist.save()

        first_item = Item()
        first_item.text = "The first (ever) list item"
        first_item.priority = "High"
        first_item.list = mylist
        first_item.save()

        second_item = Item()
        second_item.text = "Item the second"
        second_item.priority = "Low"
        second_item.list = mylist
        second_item.save()

        saved_list = List.objects.get()
        self.assertEqual(saved_list, mylist)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, "The first (ever) list item")
        self.assertEqual(first_saved_item.priority, "High")
        self.assertEqual(first_saved_item.list, mylist)
        self.assertEqual(second_saved_item.text, "Item the second")
        self.assertEqual(second_saved_item.priority, "Low")
        self.assertEqual(second_saved_item.list, mylist)

