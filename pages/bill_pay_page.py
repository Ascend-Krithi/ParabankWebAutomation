import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from locators.locators import ParabankLocators

class BillPayPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20) # Increased timeout for cloud stability

    def login(self, username, password):
        self.wait.until(EC.visibility_of_element_located(ParabankLocators.USERNAME_FIELD)).send_keys(username)
        self.driver.find_element(*ParabankLocators.PASSWORD_FIELD).send_keys(password)
        # Ensure button is clickable before clicking
        login_btn = self.wait.until(EC.element_to_be_clickable(ParabankLocators.LOGIN_BUTTON))
        login_btn.click()

    def navigate_to_bill_pay(self):
        for _ in range(3):
            try:
                self.wait.until(EC.element_to_be_clickable(ParabankLocators.BILL_PAY_LINK)).click()
                return True
            except StaleElementReferenceException:
                time.sleep(1)
        return False

    def fill_bill_pay_form(self, data):
        # Using a list of tuples to maintain order and simplify code
        fields = [
            (ParabankLocators.PAYEE_NAME, data['payee']),
            (ParabankLocators.ADDRESS, data['address']),
            (ParabankLocators.CITY, data['city']),
            (ParabankLocators.STATE, data['state']),
            (ParabankLocators.ZIP_CODE, data['zip']),
            (ParabankLocators.PHONE, data['phone']),
            (ParabankLocators.ACCOUNT_NO, data['acc']),
            (ParabankLocators.VERIFY_ACCOUNT_NO, data['acc']),
            (ParabankLocators.AMOUNT, "100")
        ]
        for locator, value in fields:
            element = self.wait.until(EC.visibility_of_element_located(locator))
            element.clear()
            element.send_keys(value)
            time.sleep(0.3) 
        
        self.driver.find_element(*ParabankLocators.SEND_PAYMENT_BTN).click()

    def get_confirmation_text(self):
        return self.wait.until(EC.visibility_of_element_located(ParabankLocators.CONFIRMATION_MSG)).text
