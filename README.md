# Makemake

## 1. Project Control Application

### Overview
This application was developed to offer comprehensive control over projects, from the creation of the initial contract to the management of price and service addendums, through detailed budget control and payments. Additionally, the system maintains a database of materials and services, facilitating the creation of accurate and detailed budgets.

### Key Features

**Project Control**
* Creation and management of projects with all pertinent information.
* Register and tracking of initial contracts for each project.

**Agreements and Addendum Management**
* Addition and management of price and service addendums to initial contracts.
* Each contract and addendum has its own detailed and individual budget.

**Budgets**
* Creation and control of detailed budgets for contracts and their addendums.
* Easy and direct inclusion of materials and services in the budgets.

**Payments**
* Control and recording of measurements (payments) made during the project.
* Complete history of all measurements and payments made.

**Supplies Database**
* Maintenance of a comprehensive database of materials and services.
* Insertion and use of these materials and services in the project budgets.

**Technologies Used**
- **Programming Language**: Python 3, Javascript
- **Markup language**: HTML 5 (is mandatory)
- **Framework**: Django 5.1 (is mandatory)

## 2. Setup

#### Preparing your enviroment

1. You must need to have Python installed on your computer (I suggest you install from an enviroment manager like conda, virtualenv, pyenv, etc)

2. Create an enviroment using virtualenv
```python3 -m venv .venv```
(please create your enviroment folders with the names .env, env, .venv or venv)

3. Activate your virtual enviroment
```source .venv/bin/activate```

4. Install project dependencies from root project and at terminal run

```pip install -r requirements.txt```

5. Duplicate a env_example file, then rename it to .env
6. Create a new secret key using secret_key_generator.py (see tools directory)

```python secret_key_generator.py```

7. Using your favorite text editor open .env file
8. Copy the new secret key for SECRET_KEY option at .env file
9. Save .env
10. Move .env for makemake directory (application)

11. At first time you must create you tables (run once) and at root project

> [!CAUTION]
> Do not run create_tables.sh if you created the virtual environment with folders with names other than .env, .venv, env, or venv. The command **find -type d -name \_\_pycache__ -exec rm -rf {} +;**
inside **create_tables** will delete essential files in this folder.

```cp tools/create_tables.sh .```

```./create_tables.sh```

During this process the admin account will be created and you must need an e-mail and password when you asked.
If you skip the step above, you need create admin account manually using

```python manage.py createsuperuser```

**Extra (trial) (optional step)**
If your are using for trial purpose, you can populate the database, copy populate.py at tools directory to project root directory than run

```cp tools/create_tables.sh```

```python populate_full.py```

Atfer tests, recreate the database running command at step 11 (above).

#### Setting your enviroment variables
1. Using your favorite text editor open makemake/.env file
2. Change DEBUG option at your convinience, True for development or False for deploy
3. Set ALLOWED_HOSTS option at your convinience ([please read ALLOWED_HOSTS section from Django website](https://docs.djangoproject.com/en/5.1/ref/settings/))
4. Save .env

## 3. Changelog

Link for [changelogs](https://github.com/cthadeusantos/makemake/CHANGELOG.md)

## 4. Known Bugs

Link for [known bugs webpage](https://github.com/cthadeusantos/makemake/KNOWNBUGS.md)

## 5. To do

Link for [TO DO webpage](https://github.com/cthadeusantos/makemake/TODO.md)

## 6. Others

**ACKNOWLEDGMENTS**
* HTML template (TailAdmin) - https://free-demo.tailadmin.com/

**LICENSE**
* This project is distributed with MIT license in the hope that it is usefull to anyone (see `LICENSE` at root). Although this project is distributed as free software, this fact do not isent it from being a scientific property. If this project aided your research, please do cite any referenced work from the authors above related in the first section of this file.