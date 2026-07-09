from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class DashboardPage:
    """Page Object para el dashboard: bienvenida, logout y lista de tareas."""

    WELCOME_MESSAGE = (By.ID, "welcome-message")
    LOGOUT_LINK = (By.ID, "logout-link")
    TASK_INPUT = (By.ID, "task-input")
    ADD_TASK_BTN = (By.ID, "add-task-btn")
    TASK_LIST = (By.ID, "task-list")
    NO_TASKS_MESSAGE = (By.ID, "no-tasks-message")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    # --- bienvenida / sesión ---

    def is_loaded(self):
        self.wait.until(EC.presence_of_element_located(self.WELCOME_MESSAGE))
        return True

    def get_welcome_text(self):
        element = self.wait.until(EC.visibility_of_element_located(self.WELCOME_MESSAGE))
        return element.text

    def logout(self):
        self.driver.find_element(*self.LOGOUT_LINK).click()

    # --- tareas ---

    def add_task(self, text):
        input_field = self.wait.until(EC.visibility_of_element_located(self.TASK_INPUT))
        input_field.clear()
        input_field.send_keys(text)
        self.driver.find_element(*self.ADD_TASK_BTN).click()
        self.wait.until(EC.presence_of_element_located(self.TASK_INPUT))

    def get_task_texts(self):
        self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        items = self.driver.find_elements(
            By.CSS_SELECTOR, "#task-list li span[id^='task-text-']"
        )
        return [item.text for item in items]

    def toggle_task_by_index(self, index):
        checkboxes = self.driver.find_elements(
            By.CSS_SELECTOR, "#task-list input[type=checkbox]"
        )
        checkboxes[index].click()
        self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    def delete_task_by_index(self, index):
        delete_buttons = self.driver.find_elements(
            By.CSS_SELECTOR, "#task-list button[id^='delete-task-']"
        )
        delete_buttons[index].click()
        self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    def is_task_done(self, index):
        items = self.driver.find_elements(By.CSS_SELECTOR, "#task-list li")
        class_attr = items[index].get_attribute("class") or ""
        return "done" in class_attr

    def has_no_tasks_message(self):
        elements = self.driver.find_elements(*self.NO_TASKS_MESSAGE)
        return len(elements) > 0
