from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import time
import unittest
import os

MAX_WAIT = 5  

class NewVisitorTest(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        if test_server := os.environ.get("TEST_SERVER"):   
            self.live_server_url = "http://" + test_server 

    def tearDown(self):
        self.browser.quit()

    # Helper function ตัวใหม่: เช็คข้อมูลตามคอลัมน์ของตาราง
    def wait_for_row_in_list_table(self, row_number, item_text, priority_text):
        start_time = time.time()
        while True:  
            try:
                # หาตาราง
                table = self.browser.find_element(By.ID, "id_list_table")
                # หาแถวทั้งหมดใน tbody
                rows = table.find_elements(By.CSS_SELECTOR, "tbody tr")
                
                # ตรวจสอบว่ามีแถวเพียงพอหรือไม่
                self.assertTrue(len(rows) >= row_number, f"Row {row_number} not found in table")
                
                # ดึงแถวที่ต้องการตรวจสอบ (row_number เริ่มที่ 1 แต่ list index เริ่มที่ 0)
                row = rows[row_number - 1]
                
                # ดึงเซลล์ทั้งหมดในแถวนั้น (td)
                cells = row.find_elements(By.TAG_NAME, "td")
                
                # Column 0 = No., Column 1 = Item, Column 2 = Priority
                self.assertEqual(cells[0].text, str(row_number))
                self.assertEqual(cells[1].text, item_text)
                self.assertEqual(cells[2].text, priority_text)
                
                return
            except (AssertionError, WebDriverException) as e:  
                if time.time() - start_time > MAX_WAIT:  
                    raise e
                time.sleep(0.5)  

    def test_layout_and_styling(self):
        # Edith goes to the home page,
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        # She notices the input box is nicely centered
        inputbox = self.browser.find_element(By.ID, "id_new_item")
        self.assertAlmostEqual(
            inputbox.location["x"] + inputbox.size["width"] / 2,
            512,
            delta=30,
        )

        # She types testing without priority
        inputbox.send_keys("testing")
        inputbox.send_keys(Keys.ENTER)
        
        # Expect row 1: "testing", Priority empty (or default)
        self.wait_for_row_in_list_table(1, "testing", "")
        
        inputbox = self.browser.find_element(By.ID, "id_new_item")
        self.assertAlmostEqual(
            inputbox.location["x"] + inputbox.size["width"] / 2,
            512,
            delta=30,
        )

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
        self.browser.find_element(By.ID, "id_new_priority").send_keys(Keys.ENTER)

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
        self.browser.find_element(By.ID, "id_new_priority").send_keys(Keys.ENTER)
        
        self.wait_for_row_in_list_table(1, "Buy Wheels", "High")

        # Henry gets his own URL
        henry_list_url = self.browser.current_url
        self.assertRegex(henry_list_url, "/lists/.+")
        self.assertNotEqual(henry_list_url, jack_list_url)

        # Double check isolation
        page_text = self.browser.find_element(By.TAG_NAME, "body").text
        self.assertNotIn("Buy Gearboxes", page_text)
        self.assertIn("Buy Wheels", page_text)

if __name__ == "__main__":
    unittest.main()