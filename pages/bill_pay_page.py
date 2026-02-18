import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from locators.locators import ParabankLocators

class BillPayPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def login(self, username, password):
        self.driver.find_element(*ParabankLocators.USERNAME_FIELD).send_keys(username)
        self.driver.find_element(*ParabankLocators.PASSWORD_FIELD).send_keys(password)
        self.driver.find_element(*ParabankLocators.LOGIN_BUTTON).click()

    def navigate_to_bill_pay(self):
        for i in range(3):
            try:
                link = self.wait.until(EC.element_to_be_clickable(ParabankLocators.BILL_PAY_LINK))
                link.click()
                return True
            except StaleElementReferenceException:
                time.sleep(1)
        return False

    def enter_field_slowly(self, locator, text):
        element = self.driver.find_element(*locator)
        element.clear()
        element.send_keys(text)
        time.sleep(0.8) # Slows down each field entry

    def fill_bill_pay_form(self, data):
        self.enter_field_slowly(ParabankLocators.PAYEE_NAME, data['payee'])
        self.enter_field_slowly(ParabankLocators.ADDRESS, data['address'])
        self.enter_field_slowly(ParabankLocators.CITY, data['city'])
        self.enter_field_slowly(ParabankLocators.STATE, data['state'])
        self.enter_field_slowly(ParabankLocators.ZIP_CODE, data['zip'])
        self.enter_field_slowly(ParabankLocators.PHONE, data['phone'])
        self.enter_field_slowly(ParabankLocators.ACCOUNT_NO, data['acc'])
        self.enter_field_slowly(ParabankLocators.VERIFY_ACCOUNT_NO, data['acc'])
        self.enter_field_slowly(ParabankLocators.AMOUNT_FIELD, "100")
        
        btn = self.driver.find_element(*ParabankLocators.SEND_PAYMENT_BTN)
        btn.click()
        time.sleep(2) # Pause to see the click

    def get_confirmation_text(self):
        element = self.wait.until(EC.visibility_of_element_located(ParabankLocators.CONFIRMATION_MSG))
        return element.text
