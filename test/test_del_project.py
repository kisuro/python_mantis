import random
from model.project import Project


def test_del_project(app):
    if app.project.amount() == 0:
        app.project.create(
            Project(name="ProjectNamePre", description="testDescriptionPre"))
    projects_before = app.project.get_project_list()
    project = random.choice(projects_before)
    app.project.delete_project_by_id(project.id)
    assert len(projects_before) - 1 == app.project.amount()

