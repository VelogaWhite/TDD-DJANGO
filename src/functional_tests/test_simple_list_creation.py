from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from .base import FunctionalTest


class NewVisitorTest(FunctionalTest):

    def test_can_start_a_todo_list(self):
        # Jack goes to check out its homepage
        self.browser.get(self.live_server_url)

        # He notices the page title and header
        self.assertIn("To-Do", self.browser.title)
        header_text = self.browser.find_element(By.TAG_NAME, "h1").text
        self.assertIn("To-Do", header_text)

        # He types "Buy Gearboxes"
        inputbox = self.browser.find_element(By.ID, "id_new_item")
        self.assertEqual(inputbox.get_attribute("placeholder"), "Enter a to-do item")
        inputbox.send_keys("Buy Gearboxes")

        # He checks for Priority input
        inputbox = self.browser.find_element(By.ID, "id_new_priority")
        self.assertEqual(inputbox.get_attribute("placeholder"), "Enter a to-do priority")

        # He types "High"
        inputbox.send_keys("High")
        inputbox.send_keys(Keys.ENTER)

        # Check Row 1
        self.wait_for_row_in_list_table(1, "Buy Gearboxes", "High")

        # He enters another item "Use Gearboxes to make a Machine"
        inputbox = self.browser.find_element(By.ID, "id_new_item")
        inputbox.send_keys("Use Gearboxes to make a Machine")

        # He enters "Medium"
        inputbox = self.browser.find_element(By.ID, "id_new_priority")
        inputbox.send_keys("Medium")

        inputbox.send_keys(Keys.ENTER)

        # Check Row 1 (Still there) and Row 2 (New item)
        self.wait_for_row_in_list_table(1, "Buy Gearboxes", "High")
        self.wait_for_row_in_list_table(2, "Use Gearboxes to make a Machine", "Medium")

    def test_multiple_users_can_start_lists_at_different_urls(self):
        # Jack starts a new to-do list
        self.browser.get(self.live_server_url)
        
        # Item 1 for Jack
        self.browser.find_element(By.ID, "id_new_item").send_keys("Buy Gearboxes")
        self.browser.find_element(By.ID, "id_new_priority").send_keys("High")
        self.browser.find_element(By.ID, "id_new_item").send_keys(Keys.ENTER)

        self.wait_for_row_in_list_table(1, "Buy Gearboxes", "High")

        # Jack gets unique URL
        jack_list_url = self.browser.current_url
        self.assertRegex(jack_list_url, "/lists/.+")

        # --- New User: Henry ---
        self.browser.delete_all_cookies()
        self.browser.get(self.live_server_url)

        # Henry shouldn't see Jack's items
        page_text = self.browser.find_element(By.TAG_NAME, "body").text
        self.assertNotIn("Buy Gearboxes", page_text)

        # Henry starts his own list
        self.browser.find_element(By.ID, "id_new_item").send_keys("Buy Wheels")
        self.browser.find_element(By.ID, "id_new_priority").send_keys("High")
        self.browser.find_element(By.ID, "id_new_item").send_keys(Keys.ENTER)
        
        self.wait_for_row_in_list_table(1, "Buy Wheels", "High")

        # Henry gets his own URL
        henry_list_url = self.browser.current_url
        self.assertRegex(henry_list_url, "/lists/.+")
        self.assertNotEqual(henry_list_url, jack_list_url)

        # Double check isolation
        page_text = self.browser.find_element(By.TAG_NAME, "body").text
        self.assertNotIn("Buy Gearboxes", page_text)
        self.assertIn("Buy Wheels", page_text)
