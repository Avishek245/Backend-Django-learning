git init
git status
git commit -m "Start Django learning project"
git push
# Learning Django: A Revision Guide

This repository contains two Django projects built while learning:

- `hello/` is the first practice project. It teaches pages, templates, static files, forms, models, admin, and messages.
- `userproject/` is the next project. It adds login, logout, authentication, and a protected home page.

The goal of this file is to record what each step does and why, so it can be used for revision later.

## 1. Django vocabulary

| Term | Meaning |
| --- | --- |
| Project | The complete Django website and its global configuration. |
| App | A feature area inside a project, such as `home`. |
| View | Python code that receives a request and returns a response. |
| URLconf | The mapping from a URL path to a view. |
| Template | HTML containing Django template tags and variables. |
| Model | A Python class that describes database data. |
| Migration | A versioned database change generated from models. |
| Middleware | Code that runs during request and response processing. |

The normal request flow is:

```text
Browser -> project urls.py -> app urls.py -> view -> model/template -> response
```

## 2. Repository structure

```text
Django/
|-- hello/                         # first practice project
|   |-- manage.py                  # command-line entry point
|   |-- hello/                     # project configuration package
|   |   |-- settings.py            # installed apps, templates, database, static files
|   |   |-- urls.py                # root URLconf and admin branding
|   |   |-- asgi.py                # ASGI deployment entry point
|   |   `-- wsgi.py                # WSGI deployment entry point
|   |-- home/                      # application package
|   |   |-- views.py               # page and contact form logic
|   |   |-- urls.py                # home, about, services, contact routes
|   |   |-- models.py              # contact model
|   |   |-- admin.py               # contact model registration
|   |   |-- apps.py                # HomeConfig application definition
|   |   `-- migrations/            # database migration history
|   |-- templates/                 # base, home, about, services, contact templates
|   |-- static/                    # static files and images
|   `-- db.sqlite3                 # local SQLite database
|-- userproject/                   # second practice project
|   |-- manage.py
|   |-- userproject/               # project configuration package
|   |-- home/                      # authentication application
|   |   |-- views.py               # index, login, and logout views
|   |   |-- urls.py                # application routes
|   |   `-- migrations/            # migration history
|   |-- templates/                 # index and login templates
|   |-- static/                    # static files
|   `-- db.sqlite3
|-- .gitignore
`-- README.md
```

Every Django project has one `manage.py`. Always run it from the project directory that contains it.

## 3. Initial setup on Windows PowerShell

Create an environment for `userproject`:

```powershell
cd E:\Django\userproject
py -m venv venv
.\venv\Scripts\Activate.ps1
py -m pip install --upgrade pip
py -m pip install django
py -m django --version
```

If PowerShell blocks activation, run this once as your user:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

The `hello` project can use the same virtual environment:

```powershell
cd E:\Django\hello
py manage.py check
```

## 4. Django commands to remember

Run these from either `E:\Django\hello` or `E:\Django\userproject`:

```powershell
py manage.py runserver             # start the development server
py manage.py check                 # find configuration errors
py manage.py help                  # list commands
py manage.py migrate               # apply migrations
py manage.py makemigrations        # create migrations after model changes
py manage.py showmigrations        # show migration status
py manage.py createsuperuser       # create an admin login
py manage.py shell                 # open a Django Python shell
```

Stop the development server with `Ctrl+C`.

## 5. First project: `hello`

### 5.1 Project configuration

`hello/hello/settings.py` controls installed apps, middleware, templates, SQLite, and static files.

Important settings used here:

```python
INSTALLED_APPS = [
    'home.apps.HomeConfig',
    # Django's built-in apps...
]

ROOT_URLCONF = 'hello.urls'
TEMPLATES[0]['DIRS'] = [BASE_DIR / 'templates']
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
```

Adding `home.apps.HomeConfig` makes Django load the `home` app.

### 5.2 URL routing

`hello/hello/urls.py` includes the app routes:

```python
path('', include('home.urls'))
path('admin/', admin.site.urls)
```

`hello/home/urls.py` maps paths to view functions:

```text
/             -> views.index
/about/       -> views.about
/services/    -> views.services
/contact/     -> views.contact
/admin/       -> Django admin
```

The trailing slash matters. These patterns use `/about/`, `/services/`, and `/contact/`.

### 5.3 Views and templates

`hello/home/views.py` demonstrates three response styles:

```python
def index(request):
    return render(request, 'index.html', context)

def about(request):
    return HttpResponse('This is a about page')

def contact(request):
    # Read POST fields, save a model, show a message, then render the page.
```

Use `render()` for an HTML template and `HttpResponse()` for a direct response. The index view sends context data, which a template reads with `{{ variable }}`.

`templates/base.html` is the shared layout. Other templates extend it:

```django
{% extends 'base.html' %}
{% block title %}Contact{% endblock title %}
{% block body %}Page content{% endblock body %}
```

This avoids repeating the navbar, Bootstrap links, and message display on every page.

### 5.4 Static files

Static files are files that are not generated by a request, such as CSS, JavaScript, and images. In a template:

```django
{% load static %}
<img src="{% static 'images/example.jpg' %}" alt="Example">
```

The `hello/static/` folder currently contains an `images/` folder and `test.txt`.

### 5.5 Contact model and form

`hello/home/models.py` defines the `contact` table with name, email, phone number, message, and date fields. The contact view reads submitted form values:

```python
name = request.POST.get('name')
email = request.POST.get('email')
```

It creates and saves a model object:

```python
new_contact = ContactMessage(
    name=name,
    email=email,
    phnum=phnum,
    message=message,
    date=datetime.date.today(),
)
new_contact.save()
```

The form must include `{% csrf_token %}` for Django's CSRF protection. After saving, `messages.success()` sends a one-time success message to the template.

### 5.6 Admin

`hello/home/admin.py` registers the contact model:

```python
admin.site.register(contact)
```

Apply migrations, create an administrator, run the server, and visit `/admin/`:

```powershell
cd E:\Django\hello
py manage.py migrate
py manage.py createsuperuser
py manage.py runserver
```

## 6. Second project: `userproject`

### 6.1 Project configuration

`userproject/userproject/settings.py` has the same basic Django structure as `hello`, but its root URL module is `userproject.urls`. Its templates are loaded from:

```python
'DIRS': [BASE_DIR / 'templates']
```

### 6.2 URL routing

`userproject/userproject/urls.py` sends all non-admin routes to `home.urls`:

```python
path('', include('home.urls'))
```

Current routes in `userproject/home/urls.py`:

```text
/          -> views.index
/login     -> views.loginUser
/logout    -> views.logoutUser
/admin/    -> Django admin
```

The login and logout patterns currently do not have trailing slashes. Use `/login` and `/logout`, not `/login/` and `/logout/`.

### 6.3 Authentication flow

The home view checks whether the request user is anonymous:

```python
if request.user.is_anonymous:
    return redirect('/login')
```

The correct property is `is_anonymous`. Writing `isanonymous` causes:

```text
AttributeError: 'User' object has no attribute 'isanonymous'
```

The login flow is:

```text
POST /login -> authenticate() -> login() -> redirect('/')
```

`authenticate()` checks the username and password. `login()` stores the authenticated user in the session. The redirect must be returned:

```python
if user is not None:
    login(request, user)
    return redirect('/')
```

The logout flow calls `logout(request)` to clear the session and redirects to `/login`.

### 6.4 Testing the login flow

```powershell
cd E:\Django\userproject
py manage.py migrate
py manage.py createsuperuser
py manage.py runserver
```

Then test these steps:

1. Visit `http://127.0.0.1:8000/` while logged out. It should redirect to `/login`.
2. Submit valid credentials at `/login`. You should be redirected to `/`.
3. Visit `/logout`. The session is cleared and you return to `/login`.
4. Visit `/` again. You should be redirected to `/login`.

## 7. Model change workflow

Whenever a model changes, use this order:

```text
Edit models.py -> makemigrations -> migrate -> test the feature
```

Example:

```powershell
cd E:\Django\hello
py manage.py makemigrations home
py manage.py migrate
py manage.py showmigrations
```

Migration files belong in Git. SQLite database files are local development data and are ignored.

## 8. Debugging checklist

1. Read the exception type and the `Raised during` view.
2. Open the file and line shown in the traceback.
3. Check spelling, especially Django properties such as `is_anonymous`.
4. Check the URL pattern character by character, including trailing `/`.
5. Run `py manage.py check`.
6. Reproduce the request in the browser and inspect the terminal traceback.

Common lessons from this project:

| Error or symptom | Cause | Fix |
| --- | --- | --- |
| `'User' object has no attribute 'isanonymous'` | Wrong property spelling | Use `request.user.is_anonymous`. |
| `logout/` does not match | Pattern is `logout` without `/` | Visit `/logout` or change the pattern to `logout/`. |
| Login appears successful but home redirects again | `login(request, user)` was missing | Call `login()` and return the redirect. |
| A new model is missing from the database | Migration was not created or applied | Run `makemigrations` and `migrate`. |
| Template cannot be found | Template directory or name is wrong | Check `TEMPLATES['DIRS']` and the template path. |

## 9. Security reminders

These projects are for local learning. Before deployment:

- Move `SECRET_KEY` into an environment variable.
- Set `DEBUG = False`.
- Configure `ALLOWED_HOSTS`.
- Never commit passwords, API keys, or production database credentials.
- Use Django forms for validation and keep CSRF protection enabled.

## 10. Git workflow

Run Git commands from `E:\Django`:

```powershell
cd E:\Django
git status
git add .
git commit -m "Describe the change"
git push
```

Review `git status` before committing. The `.gitignore` should exclude virtual environments, Python cache files, SQLite databases, secrets, IDE files, and build output, while keeping source code, templates, static source files, and migration files.
