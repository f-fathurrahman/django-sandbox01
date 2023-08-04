# Notes

## Create new project

Use `django-admin` script to create a new project
```txt
django-admin startproject myproject
```

Files created:
```txt
myproject/
    manage.py
    myproject/
        __init__.py
        settings.py
        urls.py
        asgi.py
        wsgi.py
```

These files are:

- The outer `myproject/` root directory is a container for your project. Its name doesn't matter
  to Django; you can rename it to anything you like.

- `manage.py`: A command-line utility that lets you interact with this Django project in various ways.
  You can read all the details about manage.py in django-admin and manage.py.

- The inner `myproject/` directory is the actual Python package for your project.
  Its name is the Python package name you'll need to use to import anything inside
  it (e.g. `myproject.urls`).

- `myproject/__init__.py`: An empty file that tells Python that this directory should
  be considered a Python package.

- `myproject/settings.py`: Settings/configuration for this Django project.
   Django settings will tell you all about how settings work.

- `myproject/urls.py`: The URL declarations for this Django project; a "table of contents"
  of your Django-powered site. You can read more about URLs in URL dispatcher.

- `myproject/asgi.py`: An entry-point for ASGI-compatible web servers to serve
  your project. See How to deploy with ASGI for more details.

- `mysite/wsgi.py`: An entry-point for WSGI-compatible web servers to serve your project.
  See How to deploy with WSGI for more details.


## New application: `polls` app

Create a new app, under the same directory as `myproject`
```
python manage.py startapp polls
```

Files created:
```
polls/
    __init__.py
    admin.py
    apps.py
    migrations/
        __init__.py
    models.py
    tests.py
    views.py
```

First view, edit file `polls/views.py`
```python
from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")
```

This is the simplest view possible in Django.
To call the view, we need to map it to a URL - and for this we need a URLconf.

To create a URLconf in the polls directory, create a file called urls.py Your app directory should now look like:
```
polls/
    __init__.py
    admin.py
    apps.py
    migrations/
        __init__.py
    models.py
    tests.py
    urls.py
    views.py
```


File polls/urls.py
```
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index")
]
```

The next step is to point the root URLconf at the polls.urls module.
In myproject/urls.py, add an import for django.urls.include and insert
an include() in the urlpatterns list, so you have:

```python
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("polls/", include("polls.urls")),
    path("admin/", admin.site.urls),
]
```

The include() function allows referencing other URLconfs. Whenever Django encounters include(), it chops off whatever part of the URL matched up to that point and sends the remaining string to the included URLconf for further processing.

The idea behind include() is to make it easy to plug-and-play URLs. Since polls are in their own URLconf (polls/urls.py), they can be placed under “/polls/”, or under “/fun_polls/”, or under “/content/polls/”, or any other path root, and the app will still work.

NOTE:
When to use include()
 
You should always use include() when you include other URL patterns.
admin.site.urls is the only exception to this.
NOTE:


Check: runserver access localhost:8000/polls

### path() function

The path() function is passed four arguments, two required: route and view, and two optional: kwargs, and name. At this point, it’s worth reviewing what these arguments are for.

- path() argument: route

route is a string that contains a URL pattern. When processing a request, Django starts at the first pattern in urlpatterns and makes its way down the list, comparing the requested URL against each pattern until it finds one that matches.

Patterns don’t search GET and POST parameters, or the domain name. For example, in a request to https://www.example.com/myapp/, the URLconf will look for myapp/. In a request to https://www.example.com/myapp/?page=3, the URLconf will also look for myapp/.

path() argument: view

When Django finds a matching pattern, it calls the specified view function with an HttpRequest object as the first argument and any “captured” values from the route as keyword arguments. We’ll give an example of this in a bit.

- path() argument: kwargs

Arbitrary keyword arguments can be passed in a dictionary to the target view. We aren’t going to use this feature of Django in the tutorial.

- path() argument: name

Naming your URL lets you refer to it unambiguously from elsewhere in Django, especially from within templates. This powerful feature allows you to make global changes to the URL patterns of your project while only touching a single file.

When you’re comfortable with the basic request and response flow, read part 2 of this tutorial to start working with the database.


