from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
import time
import os

MAX_WAIT = 5  

class FunctionalTest(StaticLiveServerTestCase):

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
    
    def wait_for(self, fn):  
        start_time = time.time()
        while True:
            try:
                return fn()
            except (AssertionError, WebDriverException):
                if time.time() - start_time > MAX_WAIT:
                    raise
                time.sleep(0.5)

