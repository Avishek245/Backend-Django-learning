# Learning Django: userproject

A small Django learning project. The Git repository contains the Django project in `userproject/` and an earlier practice project in `hello/`.

## Repository structure

```text
Django/
|-- userproject/             # current Django project
|   |-- manage.py
|   |-- home/                # application code
|   |   |-- models.py        # database models
|   |   |-- admin.py         # admin registrations
|   |   |-- urls.py          # app routes
|   |   |-- views.py         # request handlers
|   |   `-- migrations/      # database migration files
|   |-- templates/           # HTML templates
|   |-- static/              # CSS, JavaScript, and images
|   |-- userproject/         # settings and root URLs
|   `-- db.sqlite3          # local database, ignored by Git
|-- hello/                   # earlier Django practice project
|-- .gitignore
`-- README.md
```

## First setup on Windows PowerShell

Run these commands from the repository root:

```powershell
cd E:\Django\userproject
py -m venv venv
.\venv\Scripts\Activate.ps1
py -m pip install --upgrade pip
py -m pip install django
```

If PowerShell blocks activation, run this once in PowerShell as your user:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Check the installation:

```powershell
py -m django --version
py manage.py check
```

## Run the development server

```powershell
cd E:\Django\userproject
py manage.py runserver
```

Open <http://127.0.0.1:8000/> in a browser. Stop the server with `Ctrl+C`.

## Database and migrations

This project uses SQLite. Django stores the database in `userproject/db.sqlite3`, configured in `userproject/userproject/settings.py`.

When you create or change a model in `userproject/home/models.py`, create migration files and apply them:

```powershell
cd E:\Django\userproject
py manage.py makemigrations
py manage.py migrate
```

Useful database commands:

```powershell
# Show migration status
py manage.py showmigrations

# Open the SQLite database shell, if sqlite3 is installed
py manage.py dbshell

# Create a blank migration for a manual migration
py manage.py makemigrations --empty home
```

Migration files should be committed to Git. The local `db.sqlite3` file is ignored because it is generated data.

## Create an administrator

Create a user for `/admin/`:

```powershell
cd E:\Django\userproject
py manage.py createsuperuser
```

Start the server and visit <http://127.0.0.1:8000/admin/>.

## Add a database model

Example model in `userproject/home/models.py`:

```python
from django.db import models


class Note(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
```

After adding or changing the model:

```powershell
cd E:\Django\userproject
py manage.py makemigrations home
py manage.py migrate
```

## Register a model in the Django admin

Add this to `userproject/home/admin.py`:

```python
from django.contrib import admin

from .models import Note


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ("title", "created_at")
    search_fields = ("title", "body")
```

Then run the server and open `/admin/`. The model appears after migrations have been applied and you log in as a superuser.

## URLs, views, and templates

The project URL file includes the app routes:

```python
# userproject/userproject/urls.py
path("", include("home.urls"))
```

The current app routes are:

```text
/          -> home.views.index
/login     -> home.views.loginUser
/logout    -> home.views.logoutUser
/admin/    -> Django admin
```

The home page requires authentication. Anonymous users who visit `/` are
redirected to `/login`. After a successful login, the user is authenticated
and redirected back to `/`. Logging out clears the session and redirects to
`/login`.

The `/login` and `/logout` routes currently do not include a trailing slash.
Use `/login` and `/logout`, not `/login/` or `/logout/`, unless the patterns in
`userproject/home/urls.py` are changed to include trailing slashes.

A view renders a template with Django's `render` helper:

```python
from django.shortcuts import render


def index(request):
    return render(request, "index.html")
```

Templates are stored in `userproject/templates/` and configured in `userproject/userproject/settings.py`:

```python
"DIRS": [BASE_DIR / "templates"]
```

## Static files

Static files belong in `userproject/static/`. The project currently uses:

```python
STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
```

In a template, load static files like this:

```django
{% load static %}
<link rel="stylesheet" href="{% static 'css/site.css' %}">
```

## Useful Django commands

```powershell
cd E:\Django\userproject

# List all management commands
py manage.py help

# Validate project configuration
py manage.py check

# Open a Python shell with Django loaded
py manage.py shell

# Collect static files for deployment
py manage.py collectstatic
```

## Git workflow

Run these commands from `E:\Django`:

```powershell
cd E:\Django
git init
git add .
git status
git commit -m "Start Django learning project"
git push
```

The root `.gitignore` excludes virtual environments, Python cache files, SQLite databases, secrets, IDE files, and build output. Migration files, source code, templates, and static source files remain trackable.

## Important security note

Before deploying, move `SECRET_KEY` out of `userproject/userproject/settings.py`, set `DEBUG = False`, configure `ALLOWED_HOSTS`, and use environment variables for secrets. Never commit real passwords, API keys, or production database credentials.
