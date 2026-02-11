from django.test import TestCase

class HomePageTest(TestCase):
    def test_uses_home_template(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, "home.html")

    def test_displays_calculator_widget(self):
        response = self.client.get("/")
        html = response.content.decode('utf8')
        
        # Check for the two input boxes
        self.assertIn('id="id_number_1"', html)
        self.assertIn('id="id_number_2"', html)
        
        # Check for the two buttons
        self.assertIn('id="id_btn_sum"', html)
        self.assertIn('id="id_btn_subtract"', html)