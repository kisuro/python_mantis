from suds import WebFault
from suds.client import Client

from model.project import Project


class SoapHelper:
    def __init__(self, app):
        self.app = app
        self.client = Client("http://localhost/mantisbt-1.2.20/api/soap/mantisconnect.php?wsdl")

    def can_login(self, username, password):
        # client = Client("http://localhost/mantisbt-1.2.20/api/soap/mantisconnect.php?wsdl")
        try:
            self.client.service.mc_login(username, password)
            return True
        except WebFault:
            return False

    def get_projects_list_for_user(self, username, password):
        global resp
        projects_soap = []
        try:
            resp = self.client.service.mc_projects_get_user_accessible(username, password)
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
