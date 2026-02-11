from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
import time
import os

MAX_WAIT = 5  

class CalculatorTest(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        if test_server := os.environ.get("TEST_SERVER"):   
            self.live_server_url = "http://" + test_server 

    def tearDown(self):
        self.browser.quit()

    # Changed from 'wait_for_row' to 'wait_for_result'
    def wait_for_result(self, expected_text):
        start_time = time.time()
        while True:  
            try:
                # We expect the result to be shown in an element with id="id_result"
                result_element = self.browser.find_element(By.ID, "id_result")
                self.assertIn(expected_text, result_element.text)
                return
            except (AssertionError, WebDriverException):  
                if time.time() - start_time > MAX_WAIT:  
                    raise  
                time.sleep(0.5)  

    def test_can_perform_calculations(self):
        # Jack needs to calculate some numbers.
        # He goes to the homepage of the calculator app
        self.browser.get(self.live_server_url)

        # He notices the page title and header mention "Calculator"
        self.assertIn("Calculator", self.browser.title)
        header_text = self.browser.find_element(By.TAG_NAME, "h1").text
        self.assertIn("Calculator", header_text)

        # He sees two input boxes to enter numbers
        num_input_1 = self.browser.find_element(By.ID, "id_number_1")
        num_input_2 = self.browser.find_element(By.ID, "id_number_2")
        
        self.assertEqual(num_input_1.get_attribute("placeholder"), "Enter first number")
        self.assertEqual(num_input_2.get_attribute("placeholder"), "Enter second number")

        # He types 10 into the first box and 5 into the second
        num_input_1.send_keys("10")
        num_input_2.send_keys("5")

        # He sees two buttons: "Sum" and "Subtract"
        sum_button = self.browser.find_element(By.ID, "id_btn_sum")
        sub_button = self.browser.find_element(By.ID, "id_btn_subtract")

        # He clicks the "Sum" button
        sum_button.click()

        # The page updates and shows the result "Result: 15"
        self.wait_for_result("Result: 15")

        # Satisfied with addition, he decides to test subtraction.
        # He clears the inputs and enters new numbers: 20 and 8
        num_input_1 = self.browser.find_element(By.ID, "id_number_1")
        num_input_2 = self.browser.find_element(By.ID, "id_number_2")
        
        num_input_1.clear()
        num_input_2.clear()
        
        num_input_1.send_keys("20")
        num_input_2.send_keys("8")

        # He clicks the "Subtract" button.
        # (We need to re-find the element to avoid StaleElementReferenceException if the page reloaded)
        sub_button = self.browser.find_element(By.ID, "id_btn_subtract")
        sub_button.click()

        # The page updates and shows the result "Result: 12"
        self.wait_for_result("Result: 12")