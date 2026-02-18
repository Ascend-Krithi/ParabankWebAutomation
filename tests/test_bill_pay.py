import os
import stat
import unittest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from pages.bill_pay_page import BillPayPage
from utils.testrail_handler import TestRailHandler
from locators.locators import ParabankLocators

class TestParabankBillPay(unittest.TestCase):
    
    RUN_HEADLESS = False 

    def setUp(self):
        chrome_options = Options()
        
        # If we want Headed mode, we DO NOT add the --headless argument
        if self.RUN_HEADLESS:
            chrome_options.add_argument("--headless")
        
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")

        driver_path = ChromeDriverManager().install()
        if "THIRD_PARTY_NOTICES" in driver_path:
            driver_path = os.path.join(os.path.dirname(driver_path), "chromedriver")

        os.chmod(driver_path, stat.S_IRWXU)
        service = Service(executable_path=driver_path)
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.get("https://parabank.parasoft.com/parabank/index.htm")
        self.bp_page = BillPayPage(self.driver)

    def test_bill_payment_flow(self):
        # 1. Login
        self.bp_page.login("AAVA", "ascendion@1")
        
        # 2. FAIL-PROOF WAIT: Wait for URL to change to the dashboard
        wait = WebDriverWait(self.driver, 20)
        wait.until(EC.url_contains("overview.htm"))
        
        # 3. Synchronize on the Logout Link using the new XPATH
        logout = wait.until(EC.visibility_of_element_located(ParabankLocators.LOGOUT_LINK))
        self.assertTrue(logout.is_displayed(), "Login success but Logout link not found.")

        # 4. Navigation
        self.assertTrue(self.bp_page.navigate_to_bill_pay(), "Navigation to Bill Pay failed.")

        # 5. Form Submission
        data = {
            "payee": "Electric Company", "address": "123 Main Street",
            "city": "New York", "state": "NY", "zip": "10001",
            "phone": "555-1234", "acc": "987654321"
        }
        self.bp_page.fill_bill_pay_form(data)
        
        # 6. Final Assertions
        result_text = self.bp_page.get_confirmation_text()
        self.assertIn("Bill Payment Complete", result_text)
        self.assertIn(data["payee"], result_text)
        print("✅ Test successfully executed with all assertions verified.")

    def tearDown(self):
        if self.driver:
            self.driver.quit()

    @classmethod
    def tearDownClass(cls):
        print("\n--- Finalizing TestRail Results ---")
        try:
            tr = TestRailHandler()
            tr.update_testrail_results()
        except Exception as e:
            print(f"⚠️ TestRail Update Failed: {e}")

if __name__ == "__main__":
    unittest.main()
