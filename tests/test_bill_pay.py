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
    
    # Set to False to run in 'Headed' mode via Xvfb on the cloud
    RUN_HEADLESS = False 

    def setUp(self):
        chrome_options = Options()
        if self.RUN_HEADLESS:
            chrome_options.add_argument("--headless")
        
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")

        driver_path = ChromeDriverManager().install()
        if "THIRD_PARTY_NOTICES" in driver_path:
            driver_path = os.path.join(os.path.dirname(driver_path), "chromedriver")

        # Set execute permissions for Linux runner
        os.chmod(driver_path, stat.S_IRWXU)

        service = Service(executable_path=driver_path)
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.get("https://parabank.parasoft.com/parabank/index.htm")
        self.bp_page = BillPayPage(self.driver)

    def test_bill_payment_flow(self):
        self.bp_page.login("aavademo", "Ascendion_1")
        
        wait = WebDriverWait(self.driver, 20)
        wait.until(EC.url_contains("overview.htm"))
        
        self.assertTrue(self.bp_page.navigate_to_bill_pay())
        
        data = {
            "payee": "Electric Company", "address": "123 Main Street",
            "city": "New York", "state": "NY", "zip": "10001",
            "phone": "555-1234", "acc": "987654321"
        }
        self.bp_page.fill_bill_pay_form(data)
        
        result_text = self.bp_page.get_confirmation_text()
        self.assertIn("Bill Payment Complete", result_text)
        print("✅ UI Flow finished successfully.")

    def tearDown(self):
        if self.driver:
            self.driver.quit()

    @classmethod
    def tearDownClass(cls):
        tr = TestRailHandler()
        tr.update_testrail_results()

if __name__ == "__main__":
    unittest.main()
