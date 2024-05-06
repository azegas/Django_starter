# dev_django_starter

This is a Django app that I use at the beginning of every new Django project.

It includes:

# Pre-app setup

## Set up virtual environment

On windows, we will user virtualenvwrapper - https://virtualenvwrapper.readthedocs.io/en/latest/command_ref.html

```bash
pip install virtualenvwrapper
mkvirtualenv venv
lsvirtualenv
workon venv
pip install django
pip freeze > requirements.txt
```


# App setup

## Start a basic Django project and accounts app

```bash
django-admin startproject project
django-admin startapp accounts
python manage.py migrate
python manage.py runserver

# move accounts app into apps folder
# move project files out of the original projects folder
# move manage.py into the root of the project
```

## Other minor things

- [x] basic index page
- [x] basic url routing/views
- [x] handling static files
- [x] handling css/js
- [x] way to handle secret environment variables
- [ ] basic user authentication and custom user model
- [ ] basic logging
- [ ] Basic CRUD app for reference (base detail/list templates/views) (meke app list in whcih you can specify the name of the app and it will be represented in all views/urls/etc. Like app list. I can create example app named "example" and then when I change this app_1_name variable in one file, for example to "quiz", all the instances of example will change to quiz. context predessesor maybe?)
- [x] change /admin to something else
- [ ] add messages support

# Post-app setup
## linting
## formatting
## makefile
## pre-commit
## github actions
## basic tests/coverage
## basic docker file
## A few databases set up with examples
## django debug toolbar and other crucial django packages
## devnotes snippets, mb something useful - https://github.com/azegas/devnotes/blob/master/Django/snippets/snippets-setup.md