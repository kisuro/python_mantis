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
    projects_after = app.soap.get_projects_list_for_user(app.config['webadmin']['user'], app.config['webadmin']['password'])
    # projects_after = app.project.get_project_list()
    projects_before.remove(project)
    assert sorted(projects_before, key=Project.id_or_max) == sorted(projects_after, key=Project.id_or_max)

