# main fixture class (init driver/helpers)

from selenium import webdriver
from selenium.webdriver.support.select import Select

from fixture.session import SessionHelper
# from fixture.group import GroupHelper
# from fixture.contact import ContactHelper


class Application:
    def __init__(self, browser, base_url):
        # init driver
        if browser == "firefox":
            self.wd = webdriver.Firefox(executable_path='C:/webdrivers/ffdriver/geckodriver.exe')
        elif browser == "chrome":
            self.wd = webdriver.Chrome(executable_path='C:/webdrivers/chromedriver/chromedriver.exe')
        elif browser == "ie":
            self.wd = webdriver.Ie(executable_path='C:/webdrivers/iedriver/IEDriverServer.exe')
        elif browser == "edge":
            self.wd = webdriver.Ie(executable_path='C:/webdrivers/edge/msedgedriver.exe')
        else:
            raise ValueError("Unrecognized browser %s", browser)

        # self.wd.implicitly_wait(20)
        # init our helpers
        self.session = SessionHelper(self)
        # self.group = GroupHelper(self)
        # self.contact = ContactHelper(self)
        self.base_url = base_url

    def destroy(self):
        # close driver
        self.wd.quit()

    def is_valid(self):
        try:
            self.wd.current_url
            return True
        except:
            return False

    # navigation method(s)
    def open_home_page(self):
        wd = self.wd
        wd.get(self.base_url)

    def change_field_value(self, field_name, text):
        wd = self.wd
        if text is not None:
            wd.find_element_by_name(field_name).click()
            wd.find_element_by_name(field_name).clear()
            wd.find_element_by_name(field_name).send_keys(text)

    def change_select_value(self, select_name, select_value):
        wd = self.wd
        if select_value is not None:
            wd.find_element_by_name(select_name).click()
            Select(wd.find_element_by_name(select_name)).select_by_visible_text(select_value)
            wd.find_element_by_xpath("//option[@value='" + select_value + "']").click()
