from suds import WebFault
from suds.client import Client

from model.project import Project


class SoapHelper:
    def __init__(self, app):
        self.app = app

    def wsdl_client(self):
        return Client(self.app.base_url + self.app.config['web']['wsdl'])

    def can_login(self, username, password):
        try:
            self.wsdl_client().service.mc_login(username, password)
            return True
        except WebFault:
            return False

    def get_projects_list_for_user(self, username, password):
        global resp
        projects_soap = []
        try:
            resp = self.wsdl_client().service.mc_projects_get_user_accessible(username, password)
        except WebFault as e:
            assert ("WebFault for mc_projects_get_user_accessible: " + str(e))

        if len(resp) > 0:
            for record in resp:
                id = str(record.id)
                text = record.name
                status = record.status.name
                enabled = record.enabled
                view_status = record.view_state.name
                description = record.description
                projects_soap.append(
                    Project(id=id, name=text, status=status, enabled=enabled, view_status=view_status,
                            description=description))
            return list(projects_soap)
        else:
            assert "User "+username+" has no any projects!"
