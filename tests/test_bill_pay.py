import os
import stat
import time
import subprocess # Added for video control
import unittest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager

from pages.bill_pay_page import BillPayPage
from utils.testrail_handler import TestRailHandler
from locators.locators import ParabankLocators

class TestParabankBillPay(unittest.TestCase):
    
    RUN_HEADLESS = False 
    video_process = None # To track the recorder

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

        os.chmod(driver_path, stat.S_IRWXU)
        service = Service(executable_path=driver_path)
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # 1. Load the page first
        self.driver.get("https://parabank.parasoft.com/parabank/index.htm")
        
        # 2. Start Recording AFTER page load to avoid black screen
        print("🎥 Starting video recording...")
        self.video_process = subprocess.Popen([
            'ffmpeg', '-f', 'x11grab', '-video_size', '1920x1080', '-i', ':99',
            '-codec:v', 'libx264', '-pix_fmt', 'yuv420p', '-movflags', '+faststart',
            '-r', '24', '-y', 'video_report.mp4'
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        self.bp_page = BillPayPage(self.driver)

    def test_bill_payment_flow(self):
        self.bp_page.login("AAVA", "ascendion@1")
        
        # 40s timeout for cloud stability
        wait = WebDriverWait(self.driver, 40) 
        try:
            wait.until(EC.url_contains("overview.htm"))
        except TimeoutException:
            os.makedirs("screenshots", exist_ok=True)
            self.driver.save_screenshot("screenshots/login_timeout_debug.png")
            self.fail(f"Login timed out. Current URL: {self.driver.current_url}")

        time.sleep(2)
        self.assertTrue(self.bp_page.navigate_to_bill_pay())
        
        data = {
            "payee": "Electric Company", "address": "123 Main Street",
            "city": "New York", "state": "NY", "zip": "10001",
            "phone": "555-1234", "acc": "987654321"
        }
        self.bp_page.fill_bill_pay_form(data)
        
        time.sleep(3) 
        result_text = self.bp_page.get_confirmation_text()
        self.assertIn("Bill Payment Complete", result_text)
        
        time.sleep(5) # Final buffer to show success on video

    def tearDown(self):
        # 1. Close browser
        if self.driver:
            self.driver.quit()
        
        # 2. Stop video recording gracefully
        if self.video_process:
            print("💾 Finalizing video file...")
            self.video_process.terminate()
            time.sleep(2) # Allow ffmpeg to finalize the headers

    @classmethod
    def tearDownClass(cls):
        tr = TestRailHandler()
        tr.update_testrail_results()

if __name__ == "__main__":
    unittest.main()
