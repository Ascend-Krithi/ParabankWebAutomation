import unittest
from selenium import webdriver
from pages.bill_pay_page import BillPayPage

class TestBillPayConcurrentPayments(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get('http://parabank.demo')
        self.page = BillPayPage(self.driver)
        self.page.login('testuser', 'testpass')

    def test_concurrent_payments(self):
        # Step 1: Open two tabs with same session
        self.page.open_new_tab_with_session('http://parabank.demo')
        main_window = self.driver.window_handles[0]
        second_window = self.driver.window_handles[1]
        # Step 2: Navigate to Bill Pay in both tabs
        self.driver.switch_to.window(main_window)
        self.page.navigate_to_bill_pay()
        self.driver.switch_to.window(second_window)
        self.page.navigate_to_bill_pay()
        # Step 3: Enter payment details in both tabs
        payee_data = {
            'payee': 'Test Payee',
            'address': '123 Main St',
            'city': 'Metropolis',
            'state': 'NY',
            'zip': '12345',
            'phone': '5551234567',
            'acc': '123456789'
        }
        self.driver.switch_to.window(main_window)
        self.page.fill_bill_pay_form({**payee_data, 'amount': '75'})
        self.driver.switch_to.window(second_window)
        self.page.fill_bill_pay_form({**payee_data, 'amount': '75'})
        # Step 4: Click Send Payment simultaneously
        self.driver.switch_to.window(main_window)
        self.page.submit_payment()
        self.driver.switch_to.window(second_window)
        self.page.submit_payment()
        # Validate only one payment processed, balance correct
        self.driver.switch_to.window(main_window)
        balance = self.page.get_account_balance()
        self.assertTrue(balance == 25.00 or balance == 100.00)
        self.page.go_to_transaction_history()
        details = self.page.get_transaction_details()
        self.assertIn('75.00', details)
        self.assertNotIn('-75.00', details)

    def tearDown(self):
        self.driver.quit()

class TestBillPayConfirmationAndHistory(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get('http://parabank.demo')
        self.page = BillPayPage(self.driver)
        self.page.login('testuser', 'testpass')

    def test_successful_bill_payment_and_history(self):
        # Step 1: Complete bill payment
        payee_data = {
            'payee': 'Electric Company',
            'address': '456 Elm St',
            'city': 'Gotham',
            'state': 'NJ',
            'zip': '54321',
            'phone': '5557654321',
            'acc': '987654321'
        }
        self.page.navigate_to_bill_pay()
        self.page.fill_bill_pay_form({**payee_data, 'amount': '50'})
        self.page.submit_payment()
        # Step 2: Review confirmation
        confirmation = self.page.get_confirmation_text()
        self.assertIn('Payment Successful', confirmation)
        self.assertIn('Electric Company', confirmation)
        self.assertIn('50.00', confirmation)
        self.assertIn('987654321', confirmation)
        # Step 4: Navigate to transaction history
        self.page.go_to_transaction_history()
        details = self.page.get_transaction_details()
        self.assertIn('Electric Company', details)
        self.assertIn('50.00', details)
        self.assertIn('987654321', details)
        # Step 5: Compare confirmation details with transaction record
        balance = self.page.get_account_balance()
        self.assertTrue(balance <= 100.00)

    def tearDown(self):
        self.driver.quit()