from selenium.webdriver.common.by import By

class ParabankLocators:
    # Login Elements
    USERNAME_FIELD = (By.NAME, "username")
    PASSWORD_FIELD = (By.NAME, "password")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "input[value='Log In']")
    
    # Navigation
    BILL_PAY_LINK = (By.XPATH, "//a[text()='Bill Pay']")
    
    # Bill Pay Form Elements
    PAYEE_NAME = (By.NAME, "payee.name")
    ADDRESS = (By.NAME, "payee.address.street")
    CITY = (By.NAME, "payee.address.city")
    STATE = (By.NAME, "payee.address.state")
    ZIP_CODE = (By.NAME, "payee.address.zipCode")
    PHONE = (By.NAME, "payee.phoneNumber")
    ACCOUNT_NO = (By.NAME, "payee.accountNumber")
    VERIFY_ACCOUNT_NO = (By.NAME, "verifyAccount")
    AMOUNT_FIELD = (By.NAME, "amount")
    SEND_PAYMENT_BTN = (By.CSS_SELECTOR, "input[value='Send Payment']")
    
    # Assertion Elements
    CONFIRMATION_MSG = (By.ID, "billpayResult")
