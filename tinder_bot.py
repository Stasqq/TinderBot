from selenium import webdriver
import time
from login_and_pass import login, password


class TinderBot():
    def __init__(self):
        self.driver = webdriver.Chrome()

    def login(self):
        self.open_page('https://tinder.com')
        self.click_google_login_button()
        self.google_login_window_handle()

        self.setup_latitude_and_longitude(51.171744, 22.508145)  # for easy fake gps

        self.close_after_login_popups()

    def open_page(self, page_url):
        self.driver.get(page_url)
        time.sleep(3)  # waiting for page to load

    def click_google_login_button(self):
        google_login = self.driver.find_element_by_xpath(
            '//*[@id="modal-manager"]/div/div/div[1]/div/div[3]/span/div[1]/div/button/span[2]')
        google_login.click()

    def google_login_window_handle(self):
        base_window = self.driver.window_handles[0]
        google_login_window = self.driver.window_handles[1]

        self.driver.switch_to.window(google_login_window)

        self.login_with_google_account()

        self.driver.switch_to.window(base_window)

    def login_with_google_account(self):
        self.enter_login()
        time.sleep(3)
        self.enter_password()
        time.sleep(7)

    def enter_login(self):
        email_input = self.driver.find_element_by_xpath('//*[@id="identifierId"]')
        email_input.send_keys(login)
        accept_email_button = self.driver.find_element_by_xpath(
            '/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div/div[1]/div/div')
        accept_email_button.click()

    def enter_password(self):
        password_input = self.driver.find_element_by_xpath(
            '/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div['
            '1]/div[1]/div/div/div/div/div[1]/div/div[1]/input')
        password_input.send_keys(password)
        accept_password_button = self.driver.find_element_by_xpath(
            '/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div/div[1]/div/div')
        accept_password_button.click()

    def setup_latitude_and_longitude(self, latitude, longitude):
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "accuracy": 100
        }
        response = self.driver.execute_cdp_cmd("Page.setGeolocationOverride", params)

    def close_after_login_popups(self):
        location_accept_button = self.driver.find_element_by_xpath('/html/body/div[2]/div/div/div/div/div[3]/button[1]')
        location_accept_button.click()
        notification_disable_alert = self.driver.find_element_by_xpath(
            '/html/body/div[2]/div/div/div/div/div[3]/button[2]')
        notification_disable_alert.click()
        cookies_accept_alert = self.driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div/div/div[1]/button')
        cookies_accept_alert.click()

    def run(self):
        while True:
            time.sleep(1)
            try:
                self.like()
            except Exception:
                try:
                    self.close_popup()
                except Exception:
                    self.close_match()

    def like(self):
        like_button = self.driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div/main/div[1]/div/div/div['
                                                        '1]/div/div[2]/div[4]/button')
        like_button.click()

    def dislike(self):
        dislike_button = self.driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div/main/div[1]/div/div/div['
                                                           '1]/div/div[2]/div[2]/button')
        dislike_button.click()

    def close_popup(self):
        close_button = self.driver.find_element_by_xpath('/html/body/div[2]/div/div/div[2]/button[2]')
        close_button.click()

    def close_match(self):
        close_match_button = self.driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div/main/div['
                                                               '2]/div/div/div[1]/div/div[3]/a')
        close_match_button.click()


bot = TinderBot()
bot.login()
bot.run()
