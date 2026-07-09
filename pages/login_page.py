from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LoginPage:
    """Page Object para la pantalla de inicio de sesión."""

    URL = "http://localhost:5000/login"

    USERNAME_INPUT = (By.ID, "username")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-btn")
    ERROR_MESSAGE = (By.ID, "error-message")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def open(self):
        self.driver.get(self.URL)
        self.wait.until(EC.presence_of_element_located(self.USERNAME_INPUT))

    def login(self, username, password):
        user_field = self.wait.until(
            EC.visibility_of_element_located(self.USERNAME_INPUT)
        )
        user_field.clear()
        user_field.send_keys(username)

        pass_field = self.driver.find_element(*self.PASSWORD_INPUT)
        pass_field.clear()
        pass_field.send_keys(password)

        self.driver.find_element(*self.LOGIN_BUTTON).click()

    def get_error_message(self):
        element = self.wait.until(
            EC.visibility_of_element_located(self.ERROR_MESSAGE)
        )
        return element.text
