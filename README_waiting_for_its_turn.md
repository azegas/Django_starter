

# Devnotes

# Creating a simple Django project

## TODO Handle static files (css/js)

https://github.com/azegas/CDP?tab=readme-ov-file#static-files

## TODO create html templates for error pages

https://github.com/azegas/CDP?tab=readme-ov-file#html-templates-for-error-messages

## TODO Django debug toolbar

https://github.com/azegas/CDP?tab=readme-ov-file#django-debug-toolbar

## User authentication

User authentication already exists in Django, we just have to tap into it, add it to our url's, like the [official docs](https://docs.djangoproject.com/en/5.0/topics/auth/default/#module-django.contrib.auth.views) say.

Such view's already exist:

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

We simply need to add this to our project's urls:

```python
urlpatterns = [
    path("accounts/", include("django.contrib.auth.urls")),
]
```

### Log In Page

Let's make our login page! By default, Django will look within a templates folder called `registration` for auth templates. The login template is called `login.html`.

Then create a `templates/registration/login.html` file and include the following code:

```html
<h2>Log In</h2>
<form method="post">
  {% csrf_token %}
  {{ form }}
  <button type="submit">Log In</button>
</form>
```

This code is a standard Django form using `POST` to send data and `{% csrf_token %}` tags for security concerns, namely to prevent a CSRF Attack. The form's contents are displayed with `{{ form }}`, and then we add a "submit" button.

Next, update the `settings.py` file to tell Django to look for a `templates` folder at the project level. Update the `DIRS` setting within `TEMPLATES` with the following one-line change.

```python
# django_project/settings.py
TEMPLATES = [
    {
        ...
        "DIRS": [BASE_DIR / "templates"],  # new
        ...
    },
]
```

Our login functionality now works, but we should specify where to redirect the user upon a successful login using the `LOGIN_REDIRECT_URL` setting. At the bottom of the `settings.py` file, add the following to redirect the user to the homepage.

```python
# django_project/settings.py
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"
```

If you start the Django server again with `python manage.py runserver` and navigate to our login page at `http://127.0.0.1:8000/accounts/login/`, you'll the login form.

It worked! But how do we log out? The only option currently is to go into the admin panel at `http://127.0.0.1:8000/admin/` and click the "Log Out" link in the upper right corner.

### Sign Up Page

Now that we have sorted out logging in and logging out, it is time to add a signup page to our basic Django site. If you recall, Django **does not** provide a built-in view or URL for this, so we must code up the form and the page ourselves.

To begin, create a dedicated app called accounts, which we'll use for our custom account logic.

```python
python manage.py startapp accounts
```

Make sure to add the new app to the INSTALLED_APPS setting in the django_project/settings.py file.

Then add a URL path in `django_project/urls.py` that is **above** our included Django auth app. The order is important here because Django looks for URL patterns from top-to-bottom. We want to maintain the pattern of having our user authentication logic at `accounts/` but ensure that the signup page loads first.

```python
urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),  # new
    path("accounts/", include("django.contrib.auth.urls")),
]
```

Next, create a new file called `accounts/urls.py` and add the following code:

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

Ok, now for the final step. Create a new template, `templates/registration/signup.html`, and populate it with this code that looks almost exactly like what we used for `login.html`.

```html
{% extends "base.html" %}

{% block title %}Sign Up{% endblock %}

{% block content %}
<h2>Sign Up</h2>
<form method="post">
  {% csrf_token %}
  {{ form.as_p }}
  <button type="submit">Sign Up</button>
</form>
{% endblock %}
```

We're done! To confirm it all works, spin up our local server with `python manage.py runserver` and navigate to `http://127.0.0.1:8000/accounts/signup/`.


### Password Change

Django provides a default implementation of password change functionality. To try it out, log out of your superuser account and log in with your regular user.

The default "Password change" page is located at `http://127.0.0.1:8000/accounts/password_change/`.

Enter your old password and then a new one twice. Click the "Change My Password" button, and you will be redirected to the "Password change successful" page.

If you want to customize these two password change pages to match the look and feel of your website, it is only necessary to override the existing templates. Django already provides us with the views and URLs. To do this, create two new template files in the `registration` directory:

- templates/registration/password_change_form.html
- templates/registration/password_change_done.html

Can now add a button to change password:

```html
<p><a href="{% url 'password_change' %}">Password Change</a></p>
```

### Password Reset

A password reset page is useful when a user forgets their log in information: a user can enter in their email address and receive a cryptographically secure email with a one-time link to a password reset page. This is typically available to logged-out users. Django has built-in functionality for this that only requires a small amount of configuration.

Let's add a link to the default password reset page that will be available to logged-out users.

```html
<!-- templates/home.html -->
{% extends "base.html" %}

{% block title %}Home{% endblock %}

{% block content %}
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
{% endblock %}
```

The default template is ugly and styled to match the admin but is functional. We want to try it out, but there's one problem: our regular user account does not have an email address associated with it. The default Django [UserCreationForm](https://docs.djangoproject.com/en/5.0/topics/auth/default/#django.contrib.auth.forms.UserCreationForm) we extended for our signup form does not have email included!

Go to admin and add the email manually for now.

Django defaults to an [SMTP](https://docs.djangoproject.com/en/5.0/ref/settings/#email-backend) email backend that requires some configuration. To test the password reset flow locally, we can update the `django_project/settings.py` file to output emails to the console instead. Add this one line to the bottom of the file.

```python
# django_project/settings.py
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
```

Finally, we can try the Password Reset page again at `http://127.0.0.1:8000/accounts/password_reset/`. Enter the email address for your regular user account and click the "Change My Password" button. It will redirect you to the password reset sent page.

For security reasons, Django will not provide any notification whether you entered an email that exists in the database or not. But if you look in your terminal/console now, you can see the contents of the email outputted there.

```
Content-Type: text/plain; charset="utf-8"
MIME-Version: 1.0
Content-Transfer-Encoding: 8bit
Subject: Password reset on 127.0.0.1:8000
From: webmaster@localhost
To: hello@gmail.com
Date: Thu, 02 May 2024 13:54:13 -0000
Message-ID: <171465805380.20600.11719648789736146936@DESKTOP-AUDMJ7D.lan>


You're receiving this email because you requested a password reset for your user account at 127.0.0.1:8000.

Please go to the following page and choose a new password:

http://127.0.0.1:8000/accounts/reset/Mg/c6esad-90f0991a9e2fc27ede7e8698a7c7b4dd/

Your username, in case you’ve forgotten: gaidys

Thanks for using our site!

The 127.0.0.1:8000 team



-------------------------------------------------------------------------------
```

Copy the unique URL from your console into your web browser. It will cryptographically confirm your identity and take you to the Password Reset Confirmation page at `http://127.0.0.1:8000/accounts/reset/Mg/set-password/`.

To confirm everything worked correctly, navigate to the homepage and log in to your account with the new password.

If you want to customize the templates involved with password reset, they are located at the following locations; you need to create new template files to override them.

- templates/registration/password_reset_confirm.html
- templates/registration/password_reset_form.html
- templates/registration/password_reset_done.html

### Custom User Model

Django ships with a built-in User model for authentication and we saw how to implement login, logout, signup funcitionality above.

However, for a real-world project, [the official Django documentation](https://docs.djangoproject.com/en/5.0/topics/auth/customizing/#using-a-custom-user-model-when-starting-a-project) highly recommends using a custom user model instead; it provides far more flexibility down the line so, as a general rule, **always use a custom user model for all new Django projects**.

#### AbstractUser vs AbstractBaseUser

There are two modern ways to create a custom user model in Django: `AbstractUser` and `AbstractBaseUser`. In both cases, we can subclass them to extend existing functionality; however, `AbstractBaseUser` requires much, much more work. Seriously, only mess with it if you know what you're doing. And if you did, you wouldn't be reading this tutorial, would you?

So we'll use `AbstractUser`, which subclasses `AbstractBaseUser` but provides more default configuration.

#### Implementing Custom User Model

Previously we have created `accounts` app. In `settings.py`, we'll add the `accounts` app and use the `AUTH_USER_MODEL` config to tell Django to use our new custom user model instead of the built-in User model. We'll call our custom user model `CustomUser`.

Within INSTALLED_APPS add accounts at the bottom. Then at the bottom of the entire file, add the AUTH_USER_MODEL config.

In `settings.py`:

```python
AUTH_USER_MODEL = "accounts.CustomUser"
```

Inside of `models.py` of it, add the following:

```python
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    pass
    # add additional fields in here

    def __str__(self):
        return self.username
```

Create a new file `accounts/forms.py`. We'll update it with the following code to largely subclass the existing forms.

```python
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ("username", "email")

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ("username", "email")
```

Finally, we update `admin.py` since the admin is highly coupled to the default User model.

```python
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ["email", "username",]

admin.site.register(CustomUser, CustomUserAdmin)
```

Now we must delete the current database.

And we're done! We can now run `makemigrations` and `migrate` for the first time to create a new database that uses the custom user model.

Update the `account/views.py` to use the custom model:

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

Now that our custom user model is configured, you can quickly and at any time add additional fields. See the [Django docs](https://docs.djangoproject.com/en/5.0/topics/auth/customizing/) for further instructions.

You can also check out [DjangoX](https://github.com/wsvincent/djangox), which is an open-source Django starter framework that includes a custom user model, email/password by default instead of username/email/password, social authentication, and more.

#### Creating additional custom user model fields

To add a date of birth field to our custom user model in Django, we need to follow these steps:

1. Update your CustomUser model in `models.py`:

```python
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    date_of_birth = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.username
```

In this example, I added a date_of_birth field of type DateField with `null=True` and `blank=True` to allow users to leave it empty during registration.

2. Update forms

Since you've made changes to your user model, you should also update your custom forms to include the `date_of_birth` field. In your `forms.py`:

```python
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ("username", "email", "date_of_birth")


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ("username", "email", "date_of_birth")
```

3. Apply the migrations
4. Update the CustomUserAdmin in `admin.py`


```python
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser

    # http://127.0.0.1:8000/admin/accounts/customuser/1/change/ display modifications
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('date_of_birth',)}),
    )

    # http://127.0.0.1:8000/admin/accounts/customuser/ display modifications
    list_display = [
        "email",
        "username",
        "date_of_birth",
    ]


admin.site.register(CustomUser, CustomUserAdmin)
```
In case we want to restructure the whole admin panel view when editing a user, we can shuffle the fields as we like by modifying fieldsets:

```python
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'date_of_birth')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
```

Now when the form renders it displays a simple text type field. We can make it to a datefield simply by adding this to `CustomUserChangeForm` and `CustomUserCreationForm`:

```python
from django import forms

date_of_birth = forms.DateField(
    widget=forms.DateInput(attrs={'type': 'date'}),
)
```

Now our date_of_birth field will render nicely with a date picker.

#### Create user profile page

I would like to create a user dashboard page. Where user can see and then to modify his own profile information.

First let's create a view:

```python
# accounts/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def DashboardView(request):

    # Get the logged-in user
    user = request.user
    context = {
        "user_name": user.username,
        "user_email": user.email,
        "user_date_of_birth": user.date_of_birth,
    }

    return render(request, "registration/dashboard.html", context)
```

Then add an url:

```python
from . import views
urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("dashboard", views.DashboardView, name="dashboard"), # new
]
```

#### link to admin panel if_superuser

I want to display the link to admin panel for the users if they are superusers. Can do that simply by adding one if statement in base.html:

```html
{% if user.is_superuser %}
    <li><a class="dropdown-item" href="/admin">Admin panel</a></li>
{% endif  %}
```

#### ?next=

Not sure exactly what is the magic behind this, but I know that if I am not logged in and I try to go to http://127.0.0.1:8000/accounts/dashboard/, I get redirected to login page and the url changes to http://127.0.0.1:8000/accounts/login/?next=/accounts/dashboard/.

It is as if it says then when the user successfully completes the login procedure - redirect him/er to the initial page he/she needed, which is dashboard in this case. This is amazing.

To implement this all we have to do is:

```html
<!-- add this above the h2 Log in tag -->
{% if next %}
    {% if user.is_authenticated %}
    <p>Your account doesn't have access to this page. To proceed,
    please login with an account that has access.</p>
    {% else %}
    <p>Please login to see this page.</p>
    {% endif %}
{% endif %}

<!-- add this just below the submit button  -->
<input type="hidden" name="next" value="{{ next }}">
```

### FBV's vs CBV's?

- [FBV vs CBV?](https://github.com/azegas/quotes/issues/6)
- Would choose function based views if I could.
- Very good point for function based views (you can SEE stuff, there is NO magic) - https://youtu.be/mKzStOGIc4A?si=CP2ReqI-RNIdZirc&t=286
- can choose function based views when I need them anyway, at any time

CBV's

- Karina chooses CBV's almost all the time.
- Shipping project is also full of CBV's (django admin)
- good for large codebases
- leveling up in OOP
- goal is to be good at OOP
- good resource is out there, means that I am not the only one using CBV's ;)

[FBV > CBV's](https://roman.pt/posts/django-views-and-service-functions/):
> Serving a noble purpose of code de-duplication, class-based views often offer the cure that is worse than the disease. The code gets messy in an attempt to save or reuse a few lines of code.

[Django CBVs seem overwhelming, because there are so many!](https://vsupalov.com/django-cbv-seem-overwhelming/):

> Just ignore all generic CBVs, and stick to the View base class! You don’t need to use anything other to use CBVs and make your project work.
> 
> If you’re new to Django, or new to using class based views, it’s completely acceptable to stick to building on top of the View class. I’d go as far, as saying that it’s recommended when starting out and the best choice if you feel overwhelmed.

[When do you use Django CBVs or FBVs?](https://vsupalov.com/django-cbv-vs-fbv-beginner/):

> Simple is better than complex
> 
> The third line in the Zen of Python is a good guiding rule, and applies in this case.
> 
> Usually, it's just easier to write your own non-generic view, than trying to use them unprepared.I prefer the class-based views which are based on the View class, unless the project is large enough that there's a lot of repetition going on

### Storing secrets in `.env` file

Install dotenv:

```bash
pip install python-dotenv`
```
Add the config in the `settings.py`:

```python
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Then you can reach the needed values like so:
SECRET_KEY = os.getenv("SECRET_KEY")
DEBUG = os.getenv("DEBUG") == "True"
```

Created `.env_template` file in which I described all the environment variables that I am going to use.

Example:

```bash
# no commas after variable declaration
# no spaces before/after =

SECRET_KEY=""
DEBUG=True

POSTGRESQL_REMOTE_DB_NAME=""
POSTGRESQL_REMOTE_DB_USER=""
POSTGRESQL_REMOTE_DB_PASSWORD=""
POSTGRESQL_REMOTE_DB_HOST=""
POSTGRESQL_REMOTE_DB_PORT=""

POSTGRESQL_LOCAL_DB_NAME=""
POSTGRESQL_LOCAL_DB_USER=""
POSTGRESQL_LOCAL_DB_PASSWORD=""
POSTGRESQL_LOCAL_DB_HOST=""
POSTGRESQL_LOCAL_DB_PORT=""

MYSQL_LOCAL_DB_NAME=""
MYSQL_LOCAL_DB_USER=""
MYSQL_LOCAL_DB_PASSWORD=""
```

I also have another `.env` file, which has the actual values of the variables.

### Add logging to the django app

- [Best logging tut](https://www.youtube.com/watch?v=XSwIUnGXrwY&ab_channel=BetterStack)
- [DjangoCon 2019 talk about logging](https://www.youtube.com/watch?v=ziegOuE7M4A&t=1200s&ab_channel=DjangoConUS)
- Find all of the loggers [here](https://docs.djangoproject.com/en/5.0/ref/logging/#django-logging-extensions). Get to know to root logger - "django", then db logger - "django.db.backends" and similar.
- [Example how I added logging in quotes app](https://github.com/azegas/quotes/commit/c9070b35a2e0b36e64fc9c3abc9588ea8f9eaa36)


Nobody is paying us to log, but it is needed, just as tests. 

FIND and REPLACE all your print() with logger.info() or logger.debu().

Whenever you have shippable code, don't remove the debug logs.. no developer will run your code with debug logs on. And if there is a need for that - they will be glad that there are some debug logs in the code, that can act as a reminder and a great help to debug.

You can log your own log messages or log django's log messages as well. These are two different things.

**Loggers** - what to log

**Handlers** - how to log those logged logs

**Formatters** - how to display the logged logs 

For example here is how to log out to a file your own log message. Add the logging configuration below to your `settings.py` file:

First let's make sure the logging directory exists:

```python
# LOGGING START

LOGS_DIR = os.path.join(BASE_DIR, "logs")

if not os.path.exists(LOGS_DIR):
    os.makedirs(LOGS_DIR)
```

```python
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "file_handler": {
            "class": "logging.FileHandler",
            "filename": os.path.join(LOGS_DIR, "logs.log"),
            "level": "DEBUG",
            "formatter": "verbose",
        },
    },
    "loggers": {
        # unmapped aka root logger, catch logs from ALL modules (files)
        # this would show all of my written logs, like logger.error("hello!")        
        "": {
            "level": "DEBUG",
            "handlers": ["file_handler"],
        }
    },
    "formatters": {
        "simple": {
            "format": "{asctime}: {levelname} {message}",
            "style": "{",
        },
        "verbose": {
            "format": "{asctime}: {levelname} - {name} {module}.py (line {lineno:d}). {message}",
            "style": "{",
        },
    },
}
```

Now for test the above logger, see if anything is written to `debug_up.log` file, let's add this anywhere in our project:

```python
import logging
logger = logging.getLogger(__name__)
logger.debug("hello!")
logger.info("hello!")
logger.warning("hello!")
logger.error("hello!")
logger.critical("hello!")
```

You will see this in the terminal:

```log
2024-05-01 08:55:44,301: DEBUG - apps.authors.models models.py (line 20). hello!
2024-05-01 08:55:44,302: INFO - apps.authors.models models.py (line 21). hello!
2024-05-01 08:55:44,303: WARNING - apps.authors.models models.py (line 22). hello!
2024-05-01 08:55:44,304: ERROR - apps.authors.models models.py (line 23). hello!
2024-05-01 08:55:44,305: CRITICAL - apps.authors.models models.py (line 24). hello!
```

Now if you also want to display the same logs in the console(terminal), do this:

```python
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "file_handler": {
            "class": "logging.FileHandler",
            "filename": os.path.join(LOGS_DIR, "logs.log"),
            "level": "DEBUG",
            "formatter": "verbose",
        },
        "console_handler": { # new
            "class": "logging.StreamHandler", # new
            "level": "DEBUG", # new
            "formatter": "simple", # new
        },
    },
    "loggers": {
        # unmapped aka root logger, catch logs from ALL modules (files)
        # this would show all of my written logs, like logger.info("Index view accessed by user: %s", request.user.username)

        "": {
            "level": "DEBUG",
            "handlers": [
                "file_handler",
                "console_handler", # new
            ],
        },
    },
    "formatters": {
        "simple": {
            "format": "{asctime}: {levelname} {message}",
            "style": "{",
        },
        "verbose": {
            "format": "{asctime}: {levelname} - {name} {module}.py (line {lineno:d}). {message}",
            "style": "{",
        },
    },
}
```

If I wanted to see django's logs, similar to debug toolbar, I would have to play with the loggers, instead of "", I could for example write "django", then create another file for those logs. Have not played much, but it should work.

Also be aware of [logger namespacing](https://docs.djangoproject.com/en/5.0/howto/logging/#use-logger-namespacing), as well as [logger hierarchies and propagation](https://docs.djangoproject.com/en/5.0/howto/logging/#using-logger-hierarchies-and-propagation).

It also might be a good idea to store the debug levels, filenames and similar info to environment variables.

Can also later look into "log aggregation", store your logs and visualize in "prometheus" or "better stack"

It is also possible to add colors to logging, like so (have to `pip install colorlog` first). Add it to formatters, then use as a regular formatter in the console:

```python
        "colored": {
            "()": "colorlog.ColoredFormatter",
            "format": "%(log_color)s %(asctime)s: [%(levelname)s] - %(name)s %(module)s.py (line %(lineno)s). :: %(message)s",
        },
```

If you want "rotating" logs, can add such configuration:

```python
"handlers": {
    "rotating_file_handler": {
        "class": "logging.handlers.RotatingFileHandler",
            "filename": os.path.join(LOGS_DIR, "logs.log"),
        "mode": "a",
        "encoding": "utf-8",
        "formatter": "verbose",
        "backupCount": 5,
        "maxBytes": 10485760,
    },
}
```

If you want to see the SQL statements of each request, can add such logger:

```python
## catch all the SQL that is generated by django's ORM
"django.db.backends": {
    "level": "DEBUG",
    "handlers": [
        "console_handler",
        "rotating_file_handler",
    ],
},
```

If you want to see django's logs, all logs, create such logger:

```python
# catch logs from django (make this DEBUG to get loads of info)
"django": {
    "level": "INFO",
    "handlers": [
        "console_handler",
        "rotating_file_handler",
    ],
    "propagate": False,
},
```

### Create tests for the project

- [Tests example from quotes project](https://github.com/azegas/quotes/tree/master/tests)
- [Django docs for testing](https://docs.djangoproject.com/en/5.0/topics/testing/advanced/)
- [Nice resource(online free book about testing)](https://www.obeythetestinggoat.com/book/praise.forbook.html)
- [A Beginners Guide to Unit Testing in Django](https://ctrlzblog.com/a-beginners-guide-to-unit-testing-in-django?x-host=ctrlzblog.com)
- [How to Test Django Models (with Examples)](https://ctrlzblog.com/how-to-test-django-models-with-examples?x-host=ctrlzblog.com)
- [Issue in quotes project](https://github.com/azegas/quotes/issues/4)
- [Testing views tutorial](https://www.youtube.com/watch?v=hA_VxnxCHbo&list=PLbpAWbHbi5rMF2j5n6imm0enrSD9eQUaM&index=3&ab_channel=TheDumbfounds)
- [Functional tests](https://www.youtube.com/watch?v=28zdhLPZ1Zk&list=PLbpAWbHbi5rMF2j5n6imm0enrSD9eQUaM&index=6&ab_channel=TheDumbfounds)

>While writing tests are time consuming, they will save us time in the long run. Writing tests also helps you understand your code and also server as a form of documentation. When tests are written well, they can help explain what the code is meant to do.

Place all the tests in one folder. Separate files for views, forms, models, urls.

Run tests with `python manage.py test`. If you want to get more information abotut the test run you can change the *verbosity*. `python manage.py test --verbosity 2`.
  
#### Test coverage

It's nice to know which of your files miss testing. At least the first time you are writing tests, you are not sure what you should cover.. coverage shows you that. Later, if you want to force yourself to write tests for each new feature, to keep that coverage at +95%, you can implement coverage into your pre-commit or [github actions](https://github.com/azegas/quotes/commit/8821b2e41ba8d7838c30f7cacec77fccd8cc56a0).

```bash
pip install coverage
coverage run manage.py test
coverage report
coverage html
```

### Create a `Makefile` for the project

- [How to Fix Error Makefile: *** missing separator. Stop](https://www.youtube.com/watch?v=2nM6DBE0blA&ab_channel=BoostMyTool)
- [Intro to Makefile](https://www.vantage-ai.com/blog/speed-up-your-python-development-workflow-with-pre-commit-and-makefile)
- [Issue in quotes project](https://github.com/azegas/quotes/issues/4)

Allows you to create shortcuts for various long commands.. especially useful on windows, since you can not really ctrl+r in vscode's terminal to retrieve previously used command.

we use it in the terminal to run some checks for us manually during the development.

- install make on windows to C:\Program Files (x86)\GnuWin32\bin
- add the path above to user environment variables PATH
- write make in terminal to check if it's reachable/usable
- make sure this file is written with tabs, not spaces. 
- Can use "convert indentation to tabs" in vscode

In a Makefile, .PHONY is a special target that specifies a list of "phony" targets, which are targets that do not correspond to actual files. Instead, they are used to group and organize other targets, or to specify commands that should always be executed regardless of whether a file with the same name exists.

When you declare a target as .PHONY, it tells Make that the target is not a file, so Make will always execute the associated commands, even if a file with the same name exists in the directory.

An example `Makefile`:

```makefile
######################################### LINTING ##################################################

.PHONY: lint lint-apps lint-project lint-tests lint-ag_mixins

lint: lint-project lint-apps lint-tests lint-ag_mixins

lint-project:
	python -m pylint --version
	python -m pylint project --rcfile=.pylintrc

lint-apps:
	python -m pylint --version
	python -m pylint apps --rcfile=.pylintrc

lint-tests:
	python -m pylint --version
	python -m pylint tests --rcfile=.pylintrc

lint-ag_mixins:
	python -m pylint --version
	python -m pylint ag_mixins --rcfile=.pylintrc

######################################### FORMATTING ##################################################

.PHONY: black
black:
	python -m black --version
	python -m black .

######################################### TESTS ##################################################

.PHONY: test coverage
test:
	python manage.py test

# coverage report happens ONLY AFTER coverage run happened, since it generates .coverage file needed for the report
coverage:
	coverage run manage.py test & coverage report > coverage.txt

######################################### DJANGO STUFF ##################################################

.PHONY: mm m run freeze super pre pre-all
m:
	python manage.py migrate & python manage.py migrate --database=postgresql-remote & python manage.py migrate --database=postgresql-local & python manage.py migrate --database=mysql-local

mm:
	python manage.py makemigrations

run:
	python manage.py runserver

freeze:
	pip freeze > requirements.txt

super:
	python manage.py createsuperuser

pre:
	pre-commit run

pre-all:
	pre-commit run --all-files
```

### Set up PostgreSQL DB locally

- https://github.com/azegas/quotes/issues/31
- [Inspiration link](https://stackpython.medium.com/how-to-start-django-project-with-a-database-postgresql-aaa1d74659d8)
- [official documentation](https://docs.djangoproject.com/en/5.0/ref/databases/#postgresql-notes)
- [postgrs on railway tut](https://www.youtube.com/watch?v=HEV1PWycOuQ&t=264s&ab_channel=DennisIvy)
- [Official docs for setting up db's/having more than one db](https://docs.djangoproject.com/en/5.0/topics/db/multi-db/)

why use railway(pay $) when you can actually install postgres db locally... follow this tut - https://stackpython.medium.com/how-to-start-django-project-with-a-database-postgresql-aaa1d74659d8

dont install pgadmin directly, install postgres, the longer route.

Never used it. Good practice. Use railway and 5$ plan for it.

Perhaps also try to set up Mysql, like at work?

### Set up mysql db locally

- https://github.com/azegas/quotes/issues/41
- [SQL Server Management Studio (SSMS) | Full Course](https://www.youtube.com/watch?v=Q8gBvsUjTLw&ab_channel=JoeyBlue)
- [How to connect Django Project to Multiple Database Management Systems (Part1/2)
](https://www.youtube.com/watch?v=dBiC9XKf4pc&ab_channel=KenBroTech)
- [Django Docs about Multiple databases](https://docs.djangoproject.com/en/5.0/topics/db/multi-db/)

Imitating work environment a little bit more? use SSMS

[downloaded, installed](https://dev.mysql.com/downloads/installer/)

apsieisiu be SSMS - MySQL workbench is a good enough tool. Su SSMS tikriausiai nepasileisiu DB ir nepanaudosiu jos per django... bent jau nezinau kaip ir tingiu aiskintis. Nebutina.

### TODO how to connect another db and how to run db instance locally

Example from work

# Dockerize a Django project

## Set up WSL

First, for docker to be installed, have to have wsl setup. Google how to set it up.

When you have it installed, some wsl commands below:

```bash
wsl --update
wsl --status
wsl --version
wsl --help
wsl.exe -l -v
wsl --list --online
wsl --install
wsl.exe --shutdown
# Terminate a specific distro:
wsl.exe -t <DistroName>
# Boot up the default distro (marked with *):
wsl.exe
# Boot up a specific distro:
wsl.exe -d <DistroName>
```

## Docker

Install docker

### The most simple container possible

Build it:

```dockerfile
FROM python:3.7
# Set default command to run a shell
CMD ["/bin/bash"]
```

Build/run it:

```bash
docker build -t simpliukas .devcontainer
docker run --rm -it simpliukas
```

### Other docker commands

```bash
docker ps
docker ps -a
docker stats
docker images

# pull an image from artifactory/dockerhub
docker pull docker-io.repo7.hello.se/python:3.10-buster

docker build -t image_name .
docker built -t image_name .devcontainer

docker run <image_id/name>
docker run -it --name my-container image_name
# destroy the container on leave
docker run --rm -it --name my-container my-python-container

# --------------------------------------------------------------------
# CONNECT TO THE DOCKER
# run in interactive mode, connect to it
docker run -ti ubuntu /bin/bash
docker run -ti ubuntu /bin/bash -c "apt update && apt upgrade -y"

# attach to already created container!!!!
docker attach <id>

# --------------------------------------------------------------------
# CLEANUP

# remove docker containers from ps -a
docker rm -f <id>
# remove docker image
docker rmi <image_name>
# delete or remove all docker data like containers, images and volumes
# delete all containers
docker rm --force `docker ps -qa`
# delte all images
docker rmi --force `docker images -aq`
# idk prune smth
docker volume prune

# --------------------------------------------------------------------
# SAVE

# save an image of container. A commit is only necessary after each
# run if you want to make a snapshot there for future use, otherwise
# the container itself will stick around for you to keep using.
docker commit <id> new_name
```

### spawn ubuntu, delete when closed

This command will pull the latest Ubuntu image from Docker Hub (if you don't have it locally already), and then start a new container based on that image. The -it flag allows you to interact with the container using an interactive terminal, and --rm flag removes the container when it's stopped.

```bash
# some crap below, but does what the heading says, without bash/root
docker run -it --rm ubuntu
# below is with bash, can use root, etc
docker run -it ubuntu:latest bash
apt update
apt upgrade
apt install -y python3
apt install -y python3-pip
apt install python3.10-venv
python3 -m venv venv
source venv/bin/activate
pip install django
pip install coverage
apt install git pkg-config

# authenticate with ssh to github first if it's a private repo
git clone git@github.com:azegas/quotes.git
```

## TODO Orchestration, run multiple container "swarm"

Using docker-compose.yml

Kaip darbe darom, kazka panasaus pamegink padaryk. Vienas DB, kitas Django servisas.

# Git pre/post/github actions

## Pre-commit and `.pre-commit-config.yaml` file

- [official docs](https://pre-commit.com/)
- [Issue in quotes project](https://github.com/azegas/quotes/issues/4)
- [Intro to pre-commit](https://www.vantage-ai.com/blog/speed-up-your-python-development-workflow-with-pre-commit-and-makefile)
- [big inspiration to this file](https://builtwithdjango.com/blog/improve-your-code-with-pre-commit)
- [possible pre-commit hooks](https://pre-commit.com/hooks.html)
- [can run such checks in CI also (have not tried)](https://dev.to/techishdeep/maximize-your-python-efficiency-with-pre-commit-a-complete-but-concise-guide-39a5)
- [why not to use pre-commits (valid points)](https://www.youtube.com/watch?v=RAelLqnnOp0&ab_channel=Theo-t3%E2%80%A4gg)

### How to set up pre-commit

- install the package - `pip install pre-commit`
- write the configuration like below
- in my case I am using some pre-commit hooks, some makefile thingies
- run `pre-commit install` - This command installs the pre-commit hook into your .git/hooks/pre-commit so that it will be automatically run before each commit.
- ***!!!! DON'T FORGET TO RUN `pre-commit install` COMMAND IN TERMINAL AFTER MAKING CHANGES TO THIS FILE !!!***

> to make the .git folder visible in vscode, go file -> preferences -> settings -> files.exclude and uncheck .git folder (then hide it again, so it does not show up in the searches)

can make the commit from the terminal, OR can use source-control tab in VsCode and a "commit" button. Both will run the pre-commit. Can see the output in the terminal.

the pre-commit runs only on the changed files. So for example 'isort' will only run on files changed in current commit, not ALL of the files in the project (should be able to do it manually)

to run the pre-commit manually - `pre-commit run --all-files`

### Run pre-made pre-commit hooks

Simply choose from [possible pre-commit hooks](https://pre-commit.com/hooks.html) and add them like so:

```yaml
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v3.4.0
    hooks:
      - id: check-docstring-first
      - id: check-merge-conflict
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-ast
      - id: check-added-large-files
      - id: check-symlinks
      - id: debug-statements
      - id: detect-private-key
```

### black - The uncompromising Python code formatter

all the files that you want to commit will be checked for any inconsistencies and bad styling (based on PEP 8 standard).

This hook will automatically fix those issues according to the standards

- [Issue in quotes project](https://github.com/azegas/quotes/issues/4)
- [possible black args](https://black.readthedocs.io/en/stable/usage_and_configuration/the_basics.html)
- [line length suggestions 79 vs 88](https://black.readthedocs.io/en/stable/the_black_code_style/current_style.html#line-length) - 

Have some settings in `settings.json` of vscode related to black also.

```yaml
- repo: https://github.com/ambv/black
  rev: 24.4.0
  hooks:
    - id: black
      args: ["--line-length", "79"] # "black-formatter.args": ["--line-length", "79"], in vscode
```
Can use `pyproject.toml` file to store your black configs.

### isort - sort imports alphabetically, and automatically separated into sections and by type

- [Official docs](https://pycqa.github.io/isort/)
- https://builtwithdjango.com/blog/improve-your-code-with-pre-commit#isort
- [Possible profiles to use](https://pycqa.github.io/isort/docs/configuration/profiles.html)

```yaml
- repo: https://github.com/pycqa/isort
  rev: 5.12.0
  hooks:
    - id: isort
      name: isort (python)
      args: ["--profile", "black"]
```

Can use `pyproject.toml` file to store your isort configs.

### pyupgrade - A tool to automatically upgrade syntax for newer versions

- [Official docs](https://github.com/asottile/pyupgrade)

```yaml
- repo: https://github.com/asottile/pyupgrade
  rev: v3.15.2
  hooks:
  - id: pyupgrade
```

### flake8 - Tool For Style Guide Enforcement

- [Official docs](https://flake8.pycqa.org/en/latest/)

This plugin doesn't update the file for us you have to manually fix the code to the standard OR add an exception like "# noqa: E501" for example to the piece of code
can create .flake8 file inside the repo to override some style requirements

```yaml
- repo: https://github.com/pycqa/flake8
  rev: 6.0.0
  hooks:
    - id: flake8
```

### pylint - linter and a static code analyzer

- [Issue in quotes project](https://github.com/azegas/quotes/issues/4)
- [defaults](https://github.com/pylint-dev/pylint/blob/main/pylintrc)

Pylint is just like flake8. It will check your code for any formatting issues as well as any performance issues.

The difference is that pylint is a little more thorough and more customizable.

Those two complement each other (so if you need to ignore something, you will have to ignore it twice.

For flake ignore a line with (# noqa: E501), for pylint ignore a single line with (pylint: disable=C0301).

You don't have to set both of them up, but I sleep better when I know that two unrelated programs checked my code :)

created .pylintrc, added some of my own configs to it

if you don't like the score or something, can run pylint manually with "make lint"
depends on a local pylint installation, not a github repo, like the rest

Have an extension pylint installed in VsCode to do the linting automatically, but this is for "just in case", to see those 10.00/10 ;)

My current `.pylintrc` (some rules that we want to ignore, we put them in .pylintrc file):

```bash
# my simple .pylintrc
# decided not to add all defaults from https://github.com/pylint-dev/pylint/blob/main/pylintrc, cuz basic rules like docstrings and length's are not warned about then

[MASTER]

# let's not pylint the migrations folder
ignore=migrations

[MESSAGES CONTROL]

# this makes sure that lines like such "quotes = Quote.objects.all()"
# don't throw errors like such "apps\quotes\views.py:82:20: E1101: Class 'Quote' has no 'objects' member (no-member)"
disable=no-member

[DESIGN]

# "class AuthorCreateView(CreateView):" such class declarations would throw R0901: Too many ancestors (10/7) (too-many-ancestors) warning from pylint.
# indicates that your class, AuthorCreateView, is inheriting (directly or indirectly) from more than the default allowed number of ancestor classes.
# By default, pylint sets this limit to 7, which is often exceeded in Django projects, especially when using class-based views (CBVs) that inherit from
# Django's generic views and mixins, which themselves have multiple layers of inheritance.

# This warning is a part of the pylint design checker, which aims to identify potential design issues in your code. However, in the context of Django,
# especially with CBVs, having more than 7 ancestors is not uncommon and is typically not a sign of bad design. Django's CBVs are designed to be extended
# and composed through inheritance.
max-parents=10

[FORMAT]

# Maximum number of characters on a single line.
max-line-length=79
```

```yaml
- repo: local
  hooks:
    - id: pylint
      name: pylint
      entry: pylint
      language: system
      types: [python]
      args:
        [
          "-rn", # Only display messages (warnings)
          "-sn", # Don't display the score
          "--rcfile=.pylintrc", # Link to config file. Tested. It is taken into consideration
        ]
```

### djlint-django - Looks for errors and inconsistencies in your HTML files.

- [Official docs](https://djlint.com/docs/configuration/)

seems unmaintained. Will try to use it anyway for now.

```yaml
- repo: https://github.com/Riverside-Healthcare/djLint
  rev: v1.34.1
  hooks:
    - id: djlint-django
```

Can use `pyproject.toml` file to store your djlint configs.

### bandit - a tool designed to find common security issues in Python code.

- [Official docs](https://github.com/PyCQA/bandit)
  
reminds that you should hide secret_keys and similar

```yaml
- repo: https://github.com/PyCQA/bandit
  rev: 1.7.8
  hooks:
    - id: bandit
```

### run local Django tests

On windows:
> For some reason, when running pre-commit over vscode's github window, it does not look into the virtual env where dotenv and psycopg2 is installed.
to fix it, I installed dotenv and psycopg2 and mysqlclient locally... not the best idea, but good enough for now

On devcontainers:
> above comments got fixed when using devcontainers. I can remove dotenv, psycopg2 and mysqlclient from global installation and it all works

```yaml
- repo: local
  hooks:
    - id: local unit tests
      name: local unit tests
      entry: python manage.py test
      language: system
      pass_filenames: false # this hook will not receive the filenames of the files being committed as arguments. It will simply run the command python manage.py test without any file context. Just as we want.
```

### TODO check for TODO's in your project with a custom pre-commit hook

- similar to here - https://dev.to/techishdeep/maximize-your-python-efficiency-with-pre-commit-a-complete-but-concise-guide-39a5
- and here - https://betterprogramming.pub/want-to-avoid-forgotten-todos-in-your-project-lets-do-it-with-git-hooks-6a1835f26cf5

## Github Actions

- https://github.com/azegas/quotes/issues/32
- [official docs](https://docs.github.com/en/actions/quickstart)
- https://www.honeybadger.io/blog/django-test-github-actions/

You're correct that splitting the workflow into multiple files may result in multiple containers being created, each running a separate job. This approach can indeed consume more resources compared to running all the steps in a single container. However, there are trade-offs to consider:

1. Isolation: Running each job in its own container provides isolation between the jobs. This can be beneficial if one job fails or experiences issues, as it won't affect the execution of other jobs.
2. Parallelism: Splitting the workflow into multiple jobs allows for parallel execution, which can reduce overall workflow runtime. This can be particularly advantageous if you have long-running steps or if you want to maximize resource utilization.
3. Maintenance: Splitting the workflow into smaller, focused files can improve maintainability and readability, as each file is dedicated to a specific task or job. This can make it easier to understand and update the workflow over time.
4. Resource Usage: While running multiple containers may consume more resources, GitHub Actions provides a generous allocation of resources for each job. Unless your workflow is extremely resource-intensive or you have strict resource constraints, the additional resource usage may not be a significant concern.

Ultimately, whether to split the workflow into multiple files depends on your project's specific requirements, preferences, and resource constraints. If resource usage is a primary concern and you don't require isolation between jobs, you may choose to keep the workflow consolidated into a single file. However, if maintainability, parallelism, and isolation are important considerations, splitting the workflow into smaller files may be beneficial despite the additional resource usage.

### Hello world examples

can start with hello-world example of github action:

```yml
name: Hello World

on:
  push:
    branches:
      - master

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    - name: Say Hello
      run: echo "Hello, world!"
```

another hello-world example:

```yml
name: GitHub Actions Demo
run-name: ${{ github.actor }} is testing out GitHub Actions 🚀
on: [push]
jobs:
  Explore-GitHub-Actions:
    runs-on: ubuntu-latest
    steps:
      - run: echo "🎉 The job was automatically triggered by a ${{ github.event_name }} event."
      - run: echo "🐧 This job is now running on a ${{ runner.os }} server hosted by GitHub!"
      - run: echo "🔎 The name of your branch is ${{ github.ref }} and your repository is ${{ github.repository }}."
      - name: Check out repository code
        uses: actions/checkout@v4
      - run: echo "💡 The ${{ github.repository }} repository has been cloned to the runner."
      - run: echo "🖥️ The workflow is now ready to test your code on the runner."
      - name: List files in the repository
        run: |
          ls ${{ github.workspace }}
      - run: echo "🍏 This job's status is ${{ job.status }}."
```

### Actual examples

So I have splitted my github actions of quotes project in 3 (just line django does it):

#### `formatters.yml`

```yml
name: Formatters

on:
  push:
    branches: [ master ]
  pull_request:
    branches: [ master ]

jobs:
  black:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: black
        uses: psf/black@stable
```

#### `linters.yml`

```yml
name: Linters

on:
  push:
    branches: [ master ]
  pull_request:
    branches: [ master ]

jobs:
  linters:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Install Make
        run: sudo apt-get install make

      - name: Install Dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Run Make Lint
        run: make lint
```

#### `tests.yml`

```yml
name: Tests

on:
  push:
    branches: [ master ]
  pull_request:
    branches: [ master ]

jobs:
  tests:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Install Dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Run Tests
        run: |
          export SECRET_KEY="34234234234fsdfsdfsdffsdfsd24324dfsdfs"
          coverage run manage.py test

      - name: Check Test Coverage
        run: |
          COVERAGE_OUTPUT=$(coverage report --skip-covered)
          COVERAGE_PERCENTAGE=$(echo "$COVERAGE_OUTPUT" | awk '/TOTAL/ {print $NF}')
          echo "coverage percentage is $COVERAGE_PERCENTAGE"
          echo COVERAGE_PERCENTAGE=$COVERAGE_PERCENTAGE >> $GITHUB_ENV

      - name: Break job if coverage is not more than 95%
        if: ${{ env.COVERAGE_PERCENTAGE < '95%' }}
        run: exit 1
```

#### Github action status badge
 
[Now can also add a badge to your repo README.md](https://docs.github.com/en/actions/monitoring-and-troubleshooting-workflows/adding-a-workflow-status-badge)

#### Run github actions locally with ACT

USE ACT!!

For half a day I have been trying to implement test coverage github action. Basically to be informed/for test to break if the coverage is below 95% or something.

You need to print out the coverage percentage, fetch it, compare to the regulation (95%) and break the job accordingly if needed.

Seemed like a mission impossible and wasted a lot of time, because I have been making comits to github to check if the workflow ran properly. And then it looks like this:

failed, failed, failed action... 20x emails about it...

Thought that there must be a better way.

And then I found [ACT](https://github.com/nektos/act)!. It basically allows you to run the github actions locally... I can't believe it.

Short reminder how it works:

Tutorial - https://www.youtube.com/watch?v=7xfDpoEBp60&ab_channel=ShawnWildermuth

- install act with winget install nektos.act (for windows) ref link here - https://nektosact.com/installation/index.html
- restart vscode/vscode terminal
- navigate to the same folder where your workflows are
- run act -l
- dont forget for secret key to input something else than "${{ secrets.SECRET_KEY }}""
- run act to run all the workflows
- for the first run - cleanup all the actions, leave only the hello_world.yml and write act -l to confirm that only that one exists, then run act to run that github action
- if you want to run a specific piece of code, take other actions away from the workflow folder and leave only the piece you want to test, this will run only the needed github action, not ALL of your github actions each time.

[or give a flag of the action to run](https://nektosact.com/usage/index.html#workflows)