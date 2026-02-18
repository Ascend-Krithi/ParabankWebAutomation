import unittest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from pages.bill_pay_page import BillPayPage
from utils.testrail_handler import TestRailHandler

class TestParabankBillPay(unittest.TestCase):
    
    def setUp(self):
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service)
        self.driver.maximize_window()
        self.driver.get("https://parabank.parasoft.com/parabank/index.htm")
        self.bp_page = BillPayPage(self.driver)

    def test_bill_payment_flow(self):
        # 1. Assert Login Page Loaded
        self.assertIn("ParaBank", self.driver.title, "Home page failed to load.")

        # 2. Perform Login and Assert Success
        self.bp_page.login("aavademo", "Ascendion_1")
        self.assertTrue(self.driver.find_element(by="link text", value="Log Out").is_displayed(), 
                        "Login was not successful.")

        # 3. Navigate and Assert Page Change
        nav_success = self.bp_page.navigate_to_bill_pay()
        self.assertTrue(nav_success, "Failed to click Bill Pay link.")
        self.assertIn("billpay.htm", self.driver.current_url, "Not on the Bill Pay page.")

        # 4. Data Entry
        data = {
            "payee": "Electric Company", "address": "123 Main Street",
            "city": "New York", "state": "NY", "zip": "10001",
            "phone": "555-1234", "acc": "987654321"
        }
        self.bp_page.fill_bill_pay_form(data)
        
        # 5. Final Assertions on Confirmation Message
        result_text = self.bp_page.get_confirmation_text()
        
        # Check overall success message
        self.assertIn("Bill Payment Complete", result_text, "Success message not found!")
        
        # Check specific details in the result
        self.assertIn(data["payee"], result_text, f"Payee {data['payee']} missing from confirmation.")
        print("Test passed with all assertions verified.")

    def tearDown(self):
        self.driver.quit()
    
    @classmethod
    def tearDownClass(cls):
        """This runs once after all tests in the class are finished."""
        print("\n--- Finalizing TestRail Results ---")
        tr = TestRailHandler()
        tr.update_testrail_results()

if __name__ == "__main__":
    unittest.main()
