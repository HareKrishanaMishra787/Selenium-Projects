from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException

SIMILAR_ACCOUNT = "foodcrushbyaarushi"
USERNAME = "tarunmishra21122002"
PASSWORD = "Krish@123"


class InstaFollower:
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(options=chrome_options)
        self.wait = WebDriverWait(self.driver, 10)

    def login(self):
        self.driver.get("https://www.instagram.com/accounts/login/")
        time.sleep(4)

        try:
            cookie_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Only allow essential cookies')]"))
            )
            cookie_button.click()
        except TimeoutException:
            pass

        username_input = self.driver.find_element(By.NAME, "username")
        password_input = self.driver.find_element(By.NAME, "password")
        username_input.send_keys(USERNAME)
        password_input.send_keys(PASSWORD)
        password_input.send_keys(Keys.ENTER)
        time.sleep(5)

        try:
            save_login_prompt = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Not now')]"))
            )
            save_login_prompt.click()
        except TimeoutException:
            pass

        try:
            notifications_prompt = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Not Now')]"))
            )
            notifications_prompt.click()
        except TimeoutException:
            pass

    def find_followers(self):
        self.driver.get(f"https://www.instagram.com/{SIMILAR_ACCOUNT}/")
        time.sleep(5)

        try:
            followers_button = self.wait.until(
                EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "followers"))
            )
            followers_button.click()
        except TimeoutException:
            print("Could not open followers list.")
            return

        time.sleep(3)


        # Scroll down to load more followers
        modal_xpath ="/html/body/div[4]/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]"
        modal = self.driver.find_element(by=By.XPATH, value=modal_xpath)

        for _ in range(10):
            self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", modal)
            time.sleep(3)

    def follow(self):
        buttons = self.driver.find_elements(By.CSS_SELECTOR,
                                            value="div.x1dm5mii > div > div > div > div > div > button")
        for button in buttons:
            try:
                print(button.text)
                button.click()
                time.sleep(4)
            except ElementClickInterceptedException:
                cancel_button = self.driver.find_element(by=By.XPATH, value="//button[contains(text(), 'Cancel')]")
                cancel_button.click()


bot = InstaFollower()
bot.login()
bot.find_followers()
bot.follow()
