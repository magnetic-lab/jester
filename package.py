name = "jester"

version = "0.0.0"

description = "Short description of the package."

build_command = "python $MAGLA_SW_ROOT/resources/rez/build_scripts/build.py --operation {install}"

requires = [
    "python",
]

private_build_requires = [
    "PyYAML"
]

def commands():
    import os
    env.PYTHONPATH.append(os.path.join(this.root, "payload"))
