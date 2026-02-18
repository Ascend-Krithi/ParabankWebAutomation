from selenium.webdriver.common.by import By

class ParabankLocators:
    # Login
    USERNAME_FIELD = (By.NAME, "username")
    PASSWORD_FIELD = (By.NAME, "password")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "input[value='Log In']")
    LOGOUT_LINK = (By.XPATH, "//a[contains(@href, 'logout.htm')]") # or (By.XPATH, "//a[text()='Log Out']")
    
    # Navigation
    BILL_PAY_LINK = (By.LINK_TEXT, "Bill Pay")
    
    # Bill Pay Form
    PAYEE_NAME = (By.NAME, "payee.name")
    ADDRESS = (By.NAME, "payee.address.street")
    CITY = (By.NAME, "payee.address.city")
    STATE = (By.NAME, "payee.address.state")
    ZIP_CODE = (By.NAME, "payee.address.zipCode")
    PHONE = (By.NAME, "payee.phoneNumber")
    ACCOUNT_NO = (By.NAME, "payee.accountNumber")
    VERIFY_ACCOUNT_NO = (By.NAME, "verifyAccount")
    AMOUNT = (By.NAME, "amount")
    SEND_PAYMENT_BTN = (By.CSS_SELECTOR, "input[value='Send Payment']")
    CONFIRMATION_MSG = (By.ID, "billpayResult")
