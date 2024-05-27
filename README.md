# Introduction to dev_django_starter

This is a Django app that I use at the beginning of every new Django project.

You can delete this readme.md file when you work on your project.

# Set up virtual environment

On windows, we will user virtualenvwrapper - https://virtualenvwrapper.readthedocs.io/en/latest/command_ref.html

```bash
pip install virtualenvwrapper
mkvirtualenv venv
lsvirtualenv
workon venv
pip install django
pip freeze > requirements.txt
```

# Start a Django project

```bash
django-admin startproject project .
python manage.py runserver
```

> We will not create and run migrations until the later point (because we will create a custom user model).

# Setting up the templates

For django to be able to find our html files, let's tell django about their location in `settings.py`, make a modification to the TEMPLATES variable t:

```python
"DIRS": [os.path.join(BASE_DIR, "templates")],
```

# Create a base template

Inside of the `templates` folder, create `base` folder and then `base.html` in it with such content:

```django
{% load static %}
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Project">    

    <title>Project</title>
</head>
    <body>
    
        <div class="container">

            <nav class="navbar navbar-expand-lg navbar-light bg-light">
                <a class="navbar-brand" href="{% url "index" %}">Project</a>
                <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNavAltMarkup" aria-controls="navbarNavAltMarkup" aria-expanded="false" aria-label="Toggle navigation">
                    <span class="navbar-toggler-icon"></span>
                </button>
                <div class="collapse navbar-collapse" id="navbarNavAltMarkup">
                <div class="navbar-nav">
                    <a class="nav-item nav-link active" href="{% url "index" %}">Home</a>
                    <a class="nav-item nav-link" href="#">Page 1</a>
                    <a class="nav-item nav-link" href="#">Page 2</a>
                    {% if user.is_superuser %}
                        <a class="nav-item nav-link" href="{% url "admin:index" %}">Admin</a>
                    {% endif %}
                </div>
                </div>
            </nav>

            {% if user.is_authenticated %}
                <p>Hi {{ user.username }}!</p>
                <p><a href="{% url 'password_change' %}">Password Change</a></p>
                <form action="{% url 'logout' %}" method="post">
                    {% csrf_token %}
                    <button type="submit">Log Out</button>
                </form>
            {% else %}
                <p>You are not logged in</p>
                <p><a href="{% url 'password_reset' %}">Password Reset</a></p>
                <p><a href="{% url 'login' %}">Log In</a></p>
            {% endif %}

            <div class="container">
                {% block content %}

                {% endblock content %}
            </div>

</body>
</html>
```

# Create an `index.html` for the project

To be able to use the index.html we have just created, we need to set up the templates correctly.

Go ahead and create `index.html` inside of the `templates/project` directory, the content of it:

```django
{% extends "base/base.html" %}

{% block content %}

<p>Hello</p>

<br>
<br>
<br>

{% endblock content %}
```

# Create a basic view for the project

```python
"""A module for project views. Currently have only index."""

from django.shortcuts import render
from django.views import View


class Index(View):
    """
    Renders an index page.
    """

    def get(self, request):
        """
        What happens when GET method knocks on this view's door.
        """

        return render(request, "project/index.html")
```

Add the view to the project's urls `project/urls.py`:

```python
path("", Index.as_view(), name="index"),
```

Do a `python manage.py runserver` now and you will be presented with the index page.

# Setup Authentication

## Django Login, Logout, Signup, Password Change, and Password Reset

In this section, we'll configure a complete [user authentication system](https://docs.djangoproject.com/en/5.0/topics/auth/) in Django consisting of login, logout, signup, password change, and password reset.

Inspiration from here - https://learndjango.com/tutorials/django-login-and-logout-tutorial

The Django `contrib` module provides built-in apps to help with development. In the `project/settings.py` file under `INSTALLED_APPS`, you can see that `auth` is listed and available to us.

```python
# project/settings.py
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",  # THIS!!!!
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]
```

To use the `auth` app, we need to add it to our project-level `project/urls.py` file. At the top, import include and create a new URL path at accounts/. You can choose a different URL path, but using accounts/ is a standard practice and requires less customization later.

```python
# project/urls.py
from django.contrib import admin
from django.urls import path, include  # new

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),  # new
]
```

The auth app we've now included provides us with multiple [authentication views](https://docs.djangoproject.com/en/5.0/topics/auth/default/#module-django.contrib.auth.views) and URLs for handling login, logout, password change, password reset, etc. It notably does not include a view and URL for signup, so we have to configure that ourselves.

```
accounts/login/ [name='login']
accounts/logout/ [name='logout']
accounts/password_change/ [name='password_change']
accounts/password_change/done/ [name='password_change_done']
accounts/password_reset/ [name='password_reset']
accounts/password_reset/done/ [name='password_reset_done']
accounts/reset/<uidb64>/<token>/ [name='password_reset_confirm']
accounts/reset/done/ [name='password_reset_complete']
```

### Log In Page

Let's make our login page! By default, Django will look within a templates folder called `registration` for auth templates. The login template is called `login.html`.

Create a new project-level directory called templates and a directory called registration within it.

Then create a `templates/registration/login.html` file with your text editor and include the following code:

```django
<!-- templates/registration/login.html -->
<h2>Log In</h2>
<form method="post">
  {% csrf_token %}
  {{ form }}
  <button type="submit">Log In</button>
</form>
```

This code is a standard Django form using `POST` to send data and `{% csrf_token %}` tags for security concerns, namely to prevent a CSRF Attack. The form's contents are displayed with `{{ form }}`, and then we add a "submit" button.

Our login functionality now works, but we should specify where to redirect the user upon a successful login using the `LOGIN_REDIRECT_URL` setting. At the bottom of the `settings.py` file, add the following to redirect the user to the homepage.

```python
# project/settings.py
LOGIN_REDIRECT_URL = "index"  # new
```

If you start the Django server again with `python manage.py runserver` and navigate to our login page at `http://127.0.0.1:8000/accounts/login/`, you'll see the login page.

We can only log in if we have a user account. And since adding a signup form is yet to come, the most straightforward approach is to make a superuser account from the command line. Quit the server with `Control+c` and then run the command `python manage.py createsuperuser`. Answer the prompts and note that your password will not appear on the screen when typing for security reasons.

```
(.venv) > python manage.py createsuperuser
Username (leave blank to use 'root'):
Email address: 
Password:
Password (again):
Superuser created successfully.
```

Now start the server again with python manage.py runserver and refresh the page at `http://127.0.0.1:8000/accounts/login/`. Enter the login info for your just-created superuser.

Our login worked because it redirected us to the homepage which we have created earlier.

But how do we log out? The only option currently is to go into the admin panel at `http://127.0.0.1:8000/admin/` and click the "Log Out" link in the upper right corner. The "Logout" link will log us out.

## Log Out Button

We already have this in our `base.html`:

```django
<form action="{% url 'logout' %}" method="post">
  {% csrf_token %}
  <button type="submit">Log Out</button>
</form>
```

Then we need to update `settings.py` with our redirect link, `LOGOUT_REDIRECT_URL`. Add it right next to our login redirect so the bottom of the `settings.py` file should look as follows:

```python
# project/settings.py
LOGIN_REDIRECT_URL = "index"
LOGOUT_REDIRECT_URL = "index"  # new
```

## Sign Up Page

Now that we have sorted out logging in and logging out, it is time to add a signup page to our basic Django site. If you recall, Django **does not** provide a built-in view or URL for this, so we must code up the form and the page ourselves.

To begin, stop the local webserver with Control+c and create a dedicated app called accounts, which we'll use for our custom account logic.

```
python manage.py startapp accounts
```

We then move the newly created `accounts` app into `apps` folder for better structure in the future. All the apps will be in one folder.

Go to `apps.py` and fix the name variable to be `name = "apps.accounts"`. From now on if we want to refernece urls of this app, we will do so by writing `apps.accounts.urls`.

Make sure to add the new app to the `INSTALLED_APPS` setting in the `project/settings.py` file:

```python
# project/settings.py
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "apps.accounts",  # new
]
```

Then add a URL path in `project/urls.py` that is **above** our included Django `auth` app. The order is important here because Django looks for URL patterns from top-to-bottom. We want to maintain the pattern of having our user authentication logic at `accounts/` but ensure that the signup page loads first.

```python
# django_project/urls.py
from django.contrib import admin
from django.urls import path, include

from project.views import Index

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("apps.accounts.urls")),  # new
    path("accounts/", include("django.contrib.auth.urls")),
    path("", Index.as_view(), name="index"),
]
```

Next, create a new file called `accounts/urls.py` with your text editor and add the following code.

```python
# accounts/urls.py
from django.urls import path

from .views import SignUpView


urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
]
```

Now for the `accounts/views.py` file:

```python
# accounts/views.py
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView


class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"
```

At the top we import [UserCreationForm](https://docs.djangoproject.com/en/5.0/topics/auth/default/#django.contrib.auth.forms.UserCreationForm), [reverse_lazy](https://docs.djangoproject.com/en/5.0/ref/urlresolvers/#reverse-lazy), and the generic class-based view [CreateView](https://docs.djangoproject.com/en/5.0/ref/class-based-views/generic-editing/#django.views.generic.edit.CreateView).

We are creating a new class called `SignUpView` that extends `CreateView`, sets the form as `UserCreationForm`, and uses the *not-yet-created* template `signup.html`. Note that we use `reverse_lazy` to redirect users to the login page upon successful registration rather than `reverse`, because *for all generic class-based views*, the URLs are not loaded when the file is imported, so we have to use the lazy form of reverse to load them later when we are sure they're available.

Ok, now for the final step. Create a new template, `templates/registration/signup.html`, and populate it with this code that looks almost exactly like what we used for `login.html`.

```django
<!-- templates/registration/signup.html -->
{% extends "base.html" %}

{% block title %}Sign Up{% endblock %}

{% block content %}
<h2>Sign up</h2>
<form method="post">
  {% csrf_token %}
  {{ form }}
  <button type="submit">Sign Up</button>
</form>
{% endblock %}
```

We're done! To confirm it all works, spin up our local server with `python manage.py runserver` and navigate to `http://127.0.0.1:8000/accounts/signup/`.

Sign up for a new account and hit the "Sign up" button. You will be redirected to the login page, `http://127.0.0.1:8000/accounts/login/`, where you can log in with your new account.

And then, after a successful login, you'll be redirected to the homepage with a personalized "Hi username!" greeting.

One of Django's most powerful features is its built-in admin, which we can use to view and edit our existing users. If you navigate to the admin page at `http://127.0.0.1:8000/admin`, a warning will indicate you are currently logged in to a non-superuser account.

Log in with your superuser account and click on "Users."

You can see the two users for our Django project, the superuser and the regular user, created via the signup form.

It is possible to customize the Django admin in many ways, but for now, we can see the basic information. Clicking on an individual `username` opens up a change user page where you can edit user information.

## Password Change

Django provides a default implementation of password change functionality. To try it out, log out of your superuser account and log in with your regular user.

The default "Password change" page is located at `http://127.0.0.1:8000/accounts/password_change/`.

Enter your old password and then a new one twice. Click the "Change My Password" button, and you will be redirected to the "Password change successful" page.

If you want to customize these two password change pages to match the look and feel of your website, it is only necessary to override the existing templates. Django already provides us with the views and URLs. To do this, create two new template files in the `registration` directory:

- `templates/registration/password_change_form.html`
- `templates/registration/password_change_done.html`

We can add a password change link to the `base.html`.

## Password Reset

A password reset page is useful when a user forgets their log in information: a user can enter in their email address and receive a cryptographically secure email with a one-time link to a password reset page. This is typically available to logged-out users. Django has built-in functionality for this that only requires a small amount of configuration.

Let's add a link to the default password reset page that will be available to logged-out users.

We can add a password reset link to the `base.html`.

Click on the link for "Password Reset."

The default template is ugly and styled to match the admin but is functional. We want to try it out, but there's one problem: *our regular user account does not have an email address associated with it*. The default Django [UserCreationForm](https://docs.djangoproject.com/en/5.0/topics/auth/default/#django.contrib.auth.forms.UserCreationForm) we extended for our signup form does not have email included!

Nonetheless, there is an easy fix. Log in to the admin, click on `Users`, and select the `username` for your regular user account to bring up the change user page where you can add an email.

Make sure to click the "Save" button at the bottom of the page. Then click the "Log Out" button in the upper right-hand corner of the admin or back on the homepage.

Django defaults to an [SMTP](https://docs.djangoproject.com/en/5.0/ref/settings/#email-backend) email backend that requires some configuration. To test the password reset flow locally, we can update the `django_project/settings.py` file to output emails to the console instead. Add this one line to the bottom of the file.

```python
# django_project/settings.py
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend" # new
```

Finally, we can try the Password Reset page again at `http://127.0.0.1:8000/accounts/password_reset/`. Enter the email address for your regular user account and click the "Change My Password" button. It will redirect you to the password reset sent page.

For security reasons, Django will not provide any notification whether you entered an email that exists in the database or not. But if you look in your terminal/console now, you can see the contents of the email outputted there.

Copy the unique URL from your console into your web browser. It will cryptographically confirm your identity and take you to the Password Reset Confirmation page at `http://127.0.0.1:8000/accounts/reset/Mg/set-password/`.

Enter in a new password and click the "Change my password" button. It will redirect you to the Password reset complete page.

To confirm everything worked correctly, navigate to the homepage and log in to your account with the new password.

If you want to customize the templates involved with password reset, they are located at the following locations; you need to create new template files to override them.

- `templates/registration/password_reset_confirm.html`
- `templates/registration/password_reset_form.html`
- `templates/registration/password_reset_done.html`



## Creating a Custom User Model

Django ships with a built-in [User model](https://docs.djangoproject.com/en/5.0/ref/contrib/auth/#django.contrib.auth.models.User) for authentication and if you'd like a basic tutorial on how to implement login, logout, signup and so on see the Django Login and Logout tutorial for more.

However, for a real-world project, the [official Django documentation](https://docs.djangoproject.com/en/5.0/topics/auth/customizing/#using-a-custom-user-model-when-starting-a-project) highly recommends using a custom user model instead; it provides far more flexibility down the line so, as a general rule, **always use a custom user model for all new Django projects**.

### AbstractUser vs AbstractBaseUser

There are two modern ways to create a custom user model in Django: `AbstractUser` and `AbstractBaseUser`. In both cases, we can subclass them to extend existing functionality; however, `AbstractBaseUser` requires **much, much more work**. Seriously, only mess with it if you know what you're doing. And if you did, you wouldn't be reading this tutorial, would you?

So we'll use `AbstractUser`, which subclasses `AbstractBaseUser` but provides more default configuration.

### Custom User Model

Creating our initial custom user model requires four steps:

- update `django_project/settings.py`
- create a new `CustomUser` model
- create new `UserCreation` and `UserChangeForm` forms
- update the admin
  
In `settings.py`, we'll use the `AUTH_USER_MODEL` config to tell Django to use our new custom user model instead of the built-in `User` model. We'll call our custom user model `CustomUser`.

```python
# project/settings.py
AUTH_USER_MODEL = "accounts.CustomUser"  # new
```

Now update `accounts/models.py` with a new User model, which we'll call `CustomUser`.


```python
"""A module to register account app models to django admin."""

from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """Account model."""

    date_of_birth = models.DateField(null=True, blank=True)
    # add additional fields in here

```

We need new versions of two form methods that receive heavy use working with users. Create a new file `accounts/forms.py`. We'll update it with the following code to largely subclass the existing forms.

```python
# accounts/forms.py
"""A module for auth page forms. They are later used in the views.py"""

from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from apps.accounts.models import CustomUser


# pylint: disable=too-few-public-methods
class CustomUserCreationForm(UserCreationForm):
    """A form for user creation"""

    class Meta:
        """Additional settings for the Meta?"""

        model = CustomUser
        fields = ("username", "email", "date_of_birth")

    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"}),
    )


# pylint: disable=too-few-public-methods
class CustomUserChangeForm(UserChangeForm):
    """A form for user change"""

    class Meta:
        """Additional settings for the Meta?"""

        model = CustomUser
        fields = ("username", "email", "date_of_birth")

    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"}),
    )
```

Finally, we update `admin.py` since the admin is highly coupled to the default User model.

```python
# accounts/admin.py

"""A module to register users app models to django admin."""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from apps.accounts.forms import CustomUserChangeForm, CustomUserCreationForm
from apps.accounts.models import CustomUser


class CustomUserAdmin(UserAdmin):
    """A modification to the default account model admin."""

    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            "Personal info",
            {"fields": ("first_name", "last_name", "email", "date_of_birth")},
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    list_display = [
        "email",
        "username",
        "date_of_birth",
    ]


admin.site.register(CustomUser, CustomUserAdmin)
```

And we're done! We can now run `makemigrations` and `migrate` for the first time to create a new database that uses the custom user model.

```
(.venv) $ python manage.py makemigrations accounts
(.venv) $ python manage.py migrate
```

The last step is our `views.py` file in the `accounts` app which will contain our signup form. We will modify the already created form.

```python
"""A module for accounts app views."""

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from apps.accounts.forms import CustomUserCreationForm


class SignUpView(CreateView):
    """Generic CBV view for account create page"""

    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"
```

Create a dashboard for the user:

```python
# accounts/views.py
@login_required
def dashboard_view(request):
    """Function based view for the user's dashboard"""

    user = request.user

    context = {
        "user_name": user.username,
        "user_email": user.email,
        "user_date_of_birth": user.date_of_birth,
    }

    return render(request, "registration/dashboard.html", context)
```

Then update the views:

```python
# accounts/urls.py
"""A module that contains all the urls for the accounts app."""

from django.urls import path

from apps.accounts.views import SignUpView, dashboard_view

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("dashboard/", dashboard_view, name="dashboard"), # new
]
```



# Tailwind CSS
https://tailwindcss.com/docs/installation/play-cdn. For development purposes, I am using a CDN.

Here is a test to make sure CDN works.

```html
<!doctype html>
<html>
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body>
  <h1 class="text-3xl font-bold underline">
    Hello world!
  </h1>
</body>
</html>
```


## Handling secret environment variables

## Create basic index page

## Handling images

## Handling css/js

## Other minor things

## Basic user authentication and custom user model

## Basic logging

## Basic CRUD

Basic CRUD app for reference (base detail/list templates/views) (meke app list in whcih you can specify the name of the app and it will be represented in all views/urls/etc. Like app list. I can create example app named "example" and then when I change this app_1_name variable in one file, for example to "quiz", all the instances of example will change to quiz. context predessesor maybe?)

## change /admin to something else
## add messages support
for logging in/out, password change, etc

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
## mkdocs for documentation