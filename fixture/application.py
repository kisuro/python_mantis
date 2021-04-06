
from selenium import webdriver
from selenium.webdriver.support.select import Select

from fixture.james import JamesHelper
from fixture.mail import MailHelper
from fixture.project import ProjectHelper
from fixture.session import SessionHelper
from fixture.signup import SignupHelper
from fixture.soap import SoapHelper


class Application:
    def __init__(self, browser, config):
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

        # self.wd.implicitly_wait(25)

        self.session = SessionHelper(self)
        self.project = ProjectHelper(self)
        self.james = JamesHelper(self)
        self.signup = SignupHelper(self)
        self.mail = MailHelper(self)
        self.soap = SoapHelper(self)
        self.config = config
        self.base_url = config['web']['baseUrl']
        self.pwd = config['webadmin']['password']

    def destroy(self):
        self.wd.quit()

    def is_valid(self):
        try:
            self.wd.current_url
            return True
        except:
            return False

    def open_home_page(self):
        wd = self.wd
        wd.get(self.base_url)

    def select_value_in_dropdown(self, select_name, value):
        wd = self.wd
        if value is not None:
            dropdown_el = wd.find_element_by_name(select_name)
            dropdown_el.click()
            dropdown_el.find_element_by_xpath(".//option[contains(text(),'" + value + "')]").click()

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

    def fill_reauth_form(self):
        wd = self.wd
        if len(wd.find_elements_by_name("reauth_form")) > 0:
            wd.find_element_by_name("password").clear()
            wd.find_element_by_name("password").send_keys(self.pwd)
            wd.find_element_by_xpath("//input[@value='Login']").click()
