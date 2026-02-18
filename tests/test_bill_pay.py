import os
import stat
import time
import unittest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager

# Internal project imports
from pages.bill_pay_page import BillPayPage
from utils.testrail_handler import TestRailHandler
from locators.locators import ParabankLocators

class TestParabankBillPay(unittest.TestCase):
    
    # Set to False to allow 'Headed' execution via Xvfb on GitHub Actions
    RUN_HEADLESS = False 

    def setUp(self):
        """Initializes the driver with failsafes for cloud execution and video recording."""
        chrome_options = Options()
        if self.RUN_HEADLESS:
            chrome_options.add_argument("--headless")
        
        # Essential flags for stability in Linux/GitHub runners
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")

        # 1. Manage Driver Path
        driver_path = ChromeDriverManager().install()
        
        # FIX: Redirect if webdriver-manager points to the NOTICES text file
        if "THIRD_PARTY_NOTICES" in driver_path:
            driver_path = os.path.join(os.path.dirname(driver_path), "chromedriver")

        # 2. FIX: Set execute permissions (required for Linux/Cloud)
        os.chmod(driver_path, stat.S_IRWXU)

        # 3. Initialize Service and Driver
        service = Service(executable_path=driver_path)
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # VIDEO BUFFER: Give the ffmpeg recorder 2 seconds to start capturing
        time.sleep(2) 
        
        self.driver.get("https://parabank.parasoft.com/parabank/index.htm")
        self.bp_page = BillPayPage(self.driver)

    def test_bill_payment_flow(self):
        """The core automation flow for Parabank Bill Pay."""
        print("🚀 Starting Login process...")
        self.bp_page.login("AAVA", "ascendion@1")
        
        # Synchronization: Wait for dashboard URL
        wait = WebDriverWait(self.driver, 25)
        try:
            wait.until(EC.url_contains("overview.htm"))
            print("✅ Login successful, redirected to Overview.")
        except TimeoutException:
            # Capture evidence if login fails
            os.makedirs("screenshots", exist_ok=True)
            self.driver.save_screenshot("screenshots/login_timeout.png")
            self.fail(f"Login timed out. Current URL: {self.driver.current_url}")

        # Navigate to Bill Pay
        self.assertTrue(self.bp_page.navigate_to_bill_pay(), "Failed to navigate to Bill Pay page.")
        
        # Form Data Entry
        data = {
            "payee": "Electric Company", "address": "123 Main Street",
            "city": "New York", "state": "NY", "zip": "10001",
            "phone": "555-1234", "acc": "987654321"
        }
        print(f"📝 Filling Bill Pay form for: {data['payee']}")
        self.bp_page.fill_bill_pay_form(data)
        
        # Final Assertions
        result_text = self.bp_page.get_confirmation_text()
        self.assertIn("Bill Payment Complete", result_text, "Confirmation message missing!")
        self.assertIn(data["payee"], result_text, "Payee name missing in confirmation!")
        
        # VIDEO BUFFER: Stay on the success screen so the client can see it in the video
        time.sleep(3)
        print("✅ UI Flow finished successfully.")

    def tearDown(self):
        """Closes the browser session."""
        if self.driver:
            self.driver.quit()

    @classmethod
    def tearDownClass(cls):
        """Runs once after all tests to sync results to TestRail with IST timestamp."""
        print("\n" + "="*50)
        print("📊 FINALIZING CLOUD EXECUTION RESULTS")
        try:
            tr = TestRailHandler()
            tr.update_testrail_results()
        except Exception as e:
            print(f"⚠️ TestRail Reporting Failed: {e}")
        print("="*50)

if __name__ == "__main__":
    unittest.main()
