# `Marcom CG Studio Candidate Test 1`

> A simple PyQT application demonstrating `Qt`'s Model/View support, `CSS` Styling, and `pytest`.

## 🚩 Table of Contents

- [Installing](#-installing)
- [Running Tests](#-running-tests)
- [Launching the Application](#-launching-the-application)
- [Original Readme](#-original-readme)

## 🔧 Installing

### 1. Navigate to the project root and install using `pip`

```sh
# normal install
python -m pip install .

# development installation (includes dependencies for testing)
python -m pip install .[dev]
```

## Running Tests

> NOTE: if you have not already, you must run the development installation shown above!

```sh
python -m pytest ./tests -v
```

## Launching the Application

```sh
python -m jacob_martinez --yaml_file ./resources/data.yml
```

## Original README

Hello,

This objectives of this test are to implement a simple `pip install` installable Qt app that displays the data found the resources directory in a hierarchical view

Minimum Acceptance criteria:
1. Test should be pip installable, including any dependancies. eg: `pip install path/to/your/test`
2. There should to be a cli entry point that accepts the path to the `data.yml` file as an argument.
3. The module should be namespaced with your first name underscore last name.
4. There should be columns for Team, First Name, Last Name and Role colums
5. Employees should be grouped under their team.
6. The test's display_label object will display: "Team: <TEAM_NAME> or Name: <FIRST_NAME> <LAST_NAME> Role: <ROLE> depending on item selected."

Bonus Points:
1. Enable sorting on clicked column property.
2. Styling.
3. Any additional polish you wish to add.
