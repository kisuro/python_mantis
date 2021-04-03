import importlib
import json
import os.path

import jsonpickle
import pytest
from fixture.application import Application
# import jsonpickle
# import random
# from fixture.db import DbFixture
#
# # define default value for variables
# from fixture.orm import ORMFixture

fixture = None
target = None


# будет определять какой блок данных мы берем из target.json (web/db)
def load_config(file):
    global target
    # check if data from target.json not loaded - load it
    if target is None:
        # find path to file and join with filename (from option "target")
        config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), file)
        # open file only while load, then autoClose
        with open(config_file) as f:
            target = json.load(f)
    return target


@pytest.fixture
def app(request):
    # define variables as global
    global fixture
    # get browser data as option (defined in run configuration "additional parameters", eg:--browser=chrome.
    # default=firefox)
    browser = request.config.getoption("--browser")
    # указываем что берем из target.json данные web блока
    web_config = load_config(request.config.getoption("--target"))['web']
    web_user = load_config(request.config.getoption("--target"))['webadmin']
    # check if fixture not loaded - load it
    if fixture is None or not fixture.is_valid():
        # load base url from target.json(web block)
        fixture = Application(browser=browser, base_url=web_config['baseUrl'])
    # load user/password from target.json(web block)
    fixture.session.ensure_login(username=web_user['user'], pwd=web_user['password'])
    return fixture


# # метод для инициализации фикстуры db
# @pytest.fixture(scope="session")
# def db(request):
#     # указываем что берем из target.json данные db блока
#     db_config = load_config(request.config.getoption("--target"))['db']
#     # класс в пакете fixture/db.py и передаем ему данные из target.json(db block) для коннекта в базе
#     dbfixture = DbFixture(host=db_config['host'], name=db_config['name'], user=db_config['user'],
#                           password=db_config['password'])
#
#     # объявляем финализатор
#     def fin():
#         dbfixture.destroy()
#
#     # регистрируем
#     request.addfinalizer(fin)
#     # возвращаем
#     return dbfixture


# # метод для инициализации фикстуры ormdb
# @pytest.fixture(scope="session")
# def ormdb(request):
#     # указываем что берем из target.json данные db блока
#     db_config = load_config(request.config.getoption("--target"))['db']
#     # класс в пакете fixture/db.py и передаем ему данные из target.json(db block) для коннекта в базе
#     ormfixture = ORMFixture(host=db_config['host'], name=db_config['name'], user=db_config['user'],
#                             password=db_config['password'])
#
#     # возвращаем
#     return ormfixture


@pytest.fixture(scope="session", autouse=True)
def stop(request):
    def fin():
        fixture.session.ensure_logout()
        fixture.destroy()

    request.addfinalizer(fin)
    return fixture


# @pytest.fixture
# def check_ui(request):
#     return request.config.getoption("--check_ui")


# run configuration - additional arguments
def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="firefox")
    parser.addoption("--target", action="store", default="target.json")
    # store_true - авто true если опция есть, false если ее нет
    # parser.addoption("--check_ui", action="store_true")


# HOOK(check https://docs.pytest.org/en/stable/parametrize.html): Implement your own parametrization scheme or
# implement some dynamism for determining the parameters or scope of a fixture. We implement inserting of testdata to
# test (e.g. test_add_group) - removing annotation pytest and change input parameter to 'data_groups' in test
def pytest_generate_tests(metafunc):
    for fixture in metafunc.fixturenames:
        if fixture.startswith("data_"):
            testdata = load_from_module(fixture[5:])
            # what we put: from - fixture, what - testdata, presented in string - ids
            metafunc.parametrize(fixture, testdata, ids=[str(x) for x in testdata])
        elif fixture.startswith("json_"):
            testdata = load_from_json(fixture[5:])
            metafunc.parametrize(fixture, testdata, ids=[str(x) for x in testdata])

#
def load_from_module(module):
    return importlib.import_module("data.%s" % module).testdata


def load_from_json(file):
    # open file
    # os.path.dirname - project dir
    # os.path.abspath(__file__) - path to file
    # "data/%s.json" % file - join path to json file
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "data/%s.json" % file)) as f:
        # read file and decode to python object (testdata)
        return jsonpickle.decode(f.read())


# # my personal method for trv to get just 1 object from json (e.g. we can use it when we need just one testdata object
# # - test_edit_group.py, etc)
# def random_json_testdata(file):
#     with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "data/%s.json" % file)) as f:
#         a = jsonpickle.decode(f.read())
#         index = random.randrange(len(a))
#         return a[int(index)]
