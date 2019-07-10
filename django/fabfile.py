#!/usr/bin/python
#run virtualenv with Python 3.5. and fabric3 -> pip install fabric3
#Call on the prompt -> #fab configure_postgress
# path project /home/<userhomedirectory>/venv-book-tuto/django
'''
django/
├── config
│   ├── __init__.py
│   ├── __pycache__
│   │   ├── __init__.cpython-35.pyc
│   │   ├── settings.cpython-35.pyc
│   │   ├── urls.cpython-35.pyc
│   │   └── wsgi.cpython-35.pyc
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── core
│   ├── admin.py
│   ├── apps.py
│   ├── __init__.py
│   ├── migrations
│   │   ├── 0001_initial.py
│   │   ├── __init__.py
│   │   └── __pycache__
│   │       ├── 0001_initial.cpython-35.pyc
│   │       └── __init__.cpython-35.pyc
│   ├── models.py
│   ├── __pycache__
│   │   ├── admin.cpython-35.pyc
│   │   ├── __init__.cpython-35.pyc
│   │   ├── models.cpython-35.pyc
│   │   ├── urls.cpython-35.pyc
│   │   └── views.cpython-35.pyc
│   ├── templates
│   │   └── core
│   │       └── movie_list.html
│   ├── tests.py
│   ├── urls.py
│   └── views.py
└── manage.py
'''
from fabric.api import *

#vars postgres
user_db = "mymdb"
password_db = "development"
db = "mymdb"

#vars git
user_git = "Blessed"
email_git = "juankarma020@gmail.com"

def start_pg():
    local("service postgresql start")
    local("service postgresql status")

def usr_postgres(command):
    return local("sudo -u postgres {} ".format(command))


def pg_create_db(database):
    return usr_postgres("psql -c \"CREATE DATABASE {};\"".format(database))


def pg_create_usr_pass(usr, passw, db):
    usr_postgres("psql -c \"CREATE USER {} WITH ENCRYPTED PASSWORD '{}';\"".format(usr, passw))
    usr_postgres("psql -c \"GRANT ALL PRIVILEGES ON DATABASE {} TO {};\"".format(db, usr))
    usr_postgres("psql -c \"ALTER USER mymdb CREATEDB;\"".format(usr))

def git_config_global():
    local("git config --global user.name '{}'".format(user_git))
    local("git config --global user.email '{}'".format(email_git))


def generate_to_apply_migrations():
    local("python manage.py makemigrations")
    local("python manage.py migrate")

def configure_postgres():
    start_pg()
    pg_create_db(db)
    pg_create_usr_pass(user_db, password_db, db)
    git_config_global()
    generate_to_apply_migrations()
    local("python manage.py createsuperuser")
    local("python manage.py runserver")

#user : blessed
#email: pussy@armyspy.com
#pass: development
#fab configure_postgres 
