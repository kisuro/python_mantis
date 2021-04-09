import re
from time import sleep


class SignupHelper:
    def __init__(self, app):
        self.app = app

    def new_user(self, username, email, password):
        wd = self.app.wd
        wd.get(self.app.base_url + "/signup_page.php")
        wd.find_element_by_name("username").send_keys(username)
        wd.find_element_by_name("email").send_keys(email)
        wd.find_element_by_css_selector("input[type='submit']").click()

        mail = self.app.mail.get_mail(username, password, "[MantisBT] Account registration")
        url = self.extract_confirmation_url(mail)

        # идем по рег ссылке из письма
        wd.get(url)
        # element = WebDriverWait(wd, 50).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[value='Update User']")))
        # не работает ExplicitWait...
        sleep(2)

        wd.find_element_by_name("password").send_keys(password)
        wd.find_element_by_name("password_confirm").send_keys(password)
        wd.find_element_by_css_selector("input[value='Update User']").click()

    def extract_confirmation_url(self, text):
        # из текста письма выдераем линку на регистрацию
        return re.search("http://.*$", text, re.MULTILINE).group(0)
