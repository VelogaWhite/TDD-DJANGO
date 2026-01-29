from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import time
import unittest

MAX_WAIT = 5  

class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    # This is your new helper method
    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:  
            try:
                table = self.browser.find_element(By.ID, "id_list_table")
                rows = table.find_elements(By.TAG_NAME, "tr")
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException):  
                if time.time() - start_time > MAX_WAIT:  
                    raise  
                time.sleep(0.5)  

    def test_can_start_a_todo_list(self):
        # Jack has heard about a cool new online to-do app.
        # He goes to check out its homepage
        self.browser.get(self.live_server_url)

        # He notices the page title and header mention to-do lists
        self.assertIn("To-Do", self.browser.title)
        header_text = self.browser.find_element(By.TAG_NAME, "h1").text
        self.assertIn("To-Do", header_text)

        # He is invited to enter a to-do item straight away
        inputbox = self.browser.find_element(By.ID, "id_new_item")
        self.assertEqual(inputbox.get_attribute("placeholder"), "Enter a to-do item")

        # He types "Buy Gearboxes" into a text box
        inputbox.send_keys("Buy Gearboxes")

        # He check for Priority
        inputbox = self.browser.find_element(By.ID, "id_new_priority")
        self.assertEqual(inputbox.get_attribute("placeholder"), "Enter a to-do priority")

        # He types "High" into a priority's text box
        inputbox.send_keys("High")

        # When he hits enter, the page updates, and now the page lists
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: Buy Gearboxes (High)")

        # There is still a text box inviting him to add another item.
        # He enters "Use Gearboxes to make a Machine"
        inputbox = self.browser.find_element(By.ID, "id_new_item")
        inputbox.send_keys("Use Gearboxes to make a Machine")

        # There is also a priority box waiting for him to add.
        # He enters "Medium"
        inputbox = self.browser.find_element(By.ID, "id_new_priority")
        inputbox.send_keys("Medium")
        inputbox.send_keys(Keys.ENTER)


        # Satisfied, he goes back to play game.
    '''
    def test_multiple_users_can_start_lists_at_different_urls(self):
        # Jack starts a new to-do list
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element(By.ID, "id_new_item")
        inputbox.send_keys("Buy Gearboxes")
        inputbox.send_keys(Keys.ENTER)
        # He check for Priority
        inputbox = self.browser.find_element(By.ID, "id_new_priority")
        inputbox.send_keys("High")
        inputbox.send_keys(Keys.ENTER)

        self.wait_for_row_in_list_table("1: Buy Gearboxes")

        # He notices that his list has a unique URL
        jack_list_url = self.browser.current_url
        self.assertRegex(jack_list_url, "/lists/.+")

        # Now a new user, Herry, comes along to the site.

        ## We delete all the browser's cookies
        ## as a way of simulating a brand new user session  
        self.browser.delete_all_cookies()

        # Francis visits the home page.  There is no sign of Edith's
        # list
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element(By.TAG_NAME, "body").text
        self.assertNotIn("Buy peacock feathers", page_text)

        # Francis starts a new list by entering a new item. He
        # is less interesting than Edith...
        inputbox = self.browser.find_element(By.ID, "id_new_item")
        inputbox.send_keys("Buy milk")
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: Buy milk")

        # Francis gets his own unique URL
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, "/lists/.+")
        self.assertNotEqual(francis_list_url, edith_list_url)

        # Again, there is no trace of Edith's list
        page_text = self.browser.find_element(By.TAG_NAME, "body").text
        self.assertNotIn("Buy peacock feathers", page_text)
        self.assertIn("Buy milk", page_text)

        # Satisfied, they both go back to sleep
    '''
if __name__ == "__main__":
    unittest.main()