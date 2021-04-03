from model.project import Project


def test_add_project(app, json_projects):
    project = json_projects
    # additional precondition: if project already exist(name)- delete before (uniq name is req)
    namelist = list()
    for i in range(len(app.project.get_project_list())):
        namelist.append(str(app.project.get_project_list()[i].name))
    if project.name in namelist:
        app.project.delete_project_by_name(project.name)
    #
    projects_before = app.project.get_project_list()
    app.project.create(project)
    assert len(projects_before) + 1 == app.project.amount()
    projects_after = app.project.get_project_list()
    projects_before.append(project)
    assert sorted(projects_before, key=Project.id_or_max) == sorted(projects_after, key=Project.id_or_max)
