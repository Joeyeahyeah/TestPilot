from selenium.webdriver.common.by import By


class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.username_loc = (By.ID, "username")
        self.password_loc = (By.ID, "password")

    def login(self, username, password):
        self.driver.find_element(*self.username_loc).send_keys(username)
        self.driver.find_element(*self.password_loc).send_keys(password)
        self.driver.find_element(By.ID, "login-btn").click()