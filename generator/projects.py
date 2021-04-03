import jsonpickle
import os.path
from model.project import Project
import random
import string
import re
import getopt
import sys



try:
    opts, args = getopt.getopt(sys.argv[1:], "n:f:", ["number of projects", "file"])
except getopt.GetoptError as err:
    getopt.usage()
    sys.exit(2)

n = 5
f = "data/projects.json"

# if parameters n/f specified
for o, a in opts:
    if o == "-n":
        n = int(a)
    elif o == "-f":
        f = a

def random_string(prefix, maxlen):
    symbols = string.ascii_letters + string.digits + string.punctuation + " " * 10
    clear_symbols = re.sub(r"[\'\\<]|\s{2}|\s$", "", symbols)
    return prefix + "".join([random.choice(clear_symbols) for i in range(random.randrange(maxlen))])


project_testdata = [
    Project(name=random_string("projectname", 10), description=random_string("desc", 15))
    for i in range(n)
]

file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", f)

# open this file
with open(file, "w") as out:
    jsonpickle.set_encoder_options("json", indent=2)
    out.write(jsonpickle.encode(project_testdata))
