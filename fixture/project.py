from model.project import Project


class ProjectHelper:
    def __init__(self, app):
        self.app = app

    def open_manage_projects_page(self):
        wd = self.app.wd
        if not (self.is_manage_project_page()):
            wd.find_element_by_link_text("Manage").click()
            self.fill_reauth_form()
            wd.find_element_by_link_text("Manage Projects").click()

    def fill_reauth_form(self):
        wd = self.app.wd
        if len(wd.find_elements_by_name("reauth_form")) > 0:
            wd.find_element_by_name("password").clear()
            wd.find_element_by_name("password").send_keys("root")
            wd.find_element_by_xpath("//input[@value='Login']").click()

    def is_manage_project_page(self):
        wd = self.app.wd
        return wd.current_url.endswith("/manage_proj_page.php")

    def is_create_project_page(self):
        wd = self.app.wd
        return wd.current_url.endswith("/manage_proj_create_page.php")

    project_cache = None

    def get_project_list(self):
        if self.project_cache is None:
            wd = self.app.wd
            self.open_manage_projects_page()
            self.project_cache = []
            for element in wd.find_elements_by_xpath("//a[contains(@href,'?project_id=')]//ancestor::tr"):
                id = element.find_element_by_xpath(".//td[1]/a").get_attribute('href').rsplit('=', 1)[1]
                text = element.find_element_by_xpath(".//td[1]").text
                status = element.find_element_by_xpath(".//td[2]").text
                if element.find_element_by_xpath(".//td[3]").text != 'X':
                    enabled = True
                else:
                    enabled = False
                view_status = element.find_element_by_xpath(".//td[4]").text
                description = element.find_element_by_xpath(".//td[5]").text
                self.project_cache.append(
                    Project(id=id, name=text, status=status, enabled=enabled, view_status=view_status,
                            description=description))
        return list(self.project_cache)

    def create(self, project):
        wd = self.app.wd
        self.open_manage_projects_page()
        wd.find_element_by_xpath("//input[@value='Create New Project']").click()
        self.fill_reauth_form()
        self.fill_project_data(project)
        wd.find_element_by_xpath("//input[@value='Add Project']").click()
        self.project_cache = None

    def fill_project_data(self, project):
        self.app.change_field_value("name", project.name)
        self.app.change_field_value("description", project.description)
        self.app.select_value_in_dropdown("status", project.status)
        self.app.select_value_in_dropdown("view_state", project.view_status)
        # можно также заполнять/менять статус и тд из выпадающих, все по аналогии...

    def amount(self):
        wd = self.app.wd
        self.open_manage_projects_page()
        return int(len(wd.find_elements_by_xpath("//a[contains(@href,'?project_id=')]//ancestor::tr")))
    project_cache = None

    def delete_project_by_id(self, id):
        self.open_manage_projects_page()
        self.select_project_by_id(id)
        self.del_proj_and_confirm()

    def delete_project_by_name(self, name):
        self.open_manage_projects_page()
        self.select_project_by_name(name)
        self.del_proj_and_confirm()

    def del_proj_and_confirm(self):
        wd = self.app.wd
        wd.find_element_by_xpath("//input[@value='Delete Project']").click()
        # confirmation
        wd.find_element_by_xpath("//input[@value='Delete Project']").click()
        # self.return_to_manage_projects_page()
        self.project_cache = None

    def select_project_by_name(self, name):
        wd = self.app.wd
        wd.find_element_by_xpath("//a[text()='" + name + "']").click()
        self.fill_reauth_form()

    def select_project_by_id(self, id):
        wd = self.app.wd
        wd.find_element_by_xpath("//a[contains(@href,'?project_id=" + id + "')]").click()
        self.fill_reauth_form()
