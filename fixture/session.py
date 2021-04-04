class SessionHelper:
    def __init__(self, app):
        self.app = app

    def login(self):
        session_config = self.app.config['webadmin']
        wd = self.app.wd
        self.app.open_home_page()
        self.app.change_field_value("username", session_config['user'])
        self.app.change_field_value("password", session_config['password'])
        wd.find_element_by_xpath("//input[@value='Login']").click()

    def logout(self):
        wd = self.app.wd
        wd.find_element_by_link_text("Logout").click()

    def ensure_logout(self):
        if self.is_logged_in():
            self.logout()

    def is_logged_in(self):
        wd = self.app.wd
        if wd.current_url == 'about:blank':
            return False
        return len(wd.find_elements_by_link_text("Logout")) > 0

    def ensure_login(self):
        if self.is_logged_in():
            if self.is_logged_in_as():
                return
            else:
                self.logout()
        self.login()

    def is_logged_in_as(self):
        session_config = self.app.config['webadmin']
        return self.get_logged_user() == session_config['user']

    def get_logged_user(self):
        wd = self.app.wd
        return wd.find_element_by_css_selector("td.login-info-left span").text
