We’re continuing the web-poll application and will focus on creating the public interface – “views.”

Overview

A view is a “type” of web page in your Django application that generally serves a specific
function and has a specific template. For example, in a blog application, you might
have the following views:

    Blog homepage – displays the latest few entries.
    Entry “detail” page – permalink page for a single entry.
    Year-based archive page – displays all months with entries in the given year.
    Month-based archive page – displays all days with entries in the given month.
    Day-based archive page – displays all entries in the given day.
    Comment action – handles posting comments to a given entry.

In our poll application, we’ll have the following four views:

    Question “index” page – displays the latest few questions.
    Question “detail” page – displays a question text, with no results but with a form to vote.
    Question “results” page – displays results for a particular question.
    Vote action – handles voting for a particular choice in a particular question.

In Django, web pages and other content are delivered by views. Each view is represented by a Python function (or method, in the case of class-based views). Django will choose a view by examining the URL that’s requested (to be precise, the part of the URL after the domain name).

Now in your time on the web you may have come across such beauties as ME2/Sites/dirmod.htm?sid=&type=gen&mod=Core+Pages&gid=A6CD4967199A42D9B65B1B. You will be pleased to know that Django allows us much more elegant URL patterns than that.

A URL pattern is the general form of a URL - for example: `/newsarchive/<year>/<month>/`.

To get from a URL to a view, Django uses what are known as ‘URLconfs’.
A URLconf maps URL patterns to views.

This tutorial provides basic instruction in the use of URLconfs, and you can refer to URL dispatcher for more information.

# Removing hardcoded URLs in templates

Remember, when we wrote the link to a question in the polls/index.html template, the link was partially hardcoded like this:

```
<li><a href="/polls/{{ question.id }}/">{{ question.question_text }}</a></li>
```

The problem with this hardcoded, tightly-coupled approach is that it becomes challenging to 
change URLs on projects with a lot of templates.
However, since you defined the name 
argument in the `path()` functions in the `polls.urls` module, you can remove a reliance on 
specific URL paths defined in your url configurations by using the `{% url %}` template tag:
```
<li><a href="{% url 'detail' question.id %}">{{ question.question_text }}</a></li>
```

The way this works is by looking up the URL definition as specified in the polls.urls module.
You can see exactly where the URL name of ‘detail’ is defined below:
```python
...
# the 'name' value as called by the {% url %} template tag
path("<int:question_id>/", views.detail, name="detail"),
...
```

If you want to change the URL of the polls detail view to something else, perhaps to something like
`polls/specifics/12/` instead of doing it in the template (or templates) you would change
it in `polls/urls.py`:
```python
...
# added the word 'specifics'
path("specifics/<int:question_id>/", views.detail, name="detail"),
...
```

# Namespacing URL names

The tutorial project has just one app, polls. In real Django projects, there might be five,
ten, twenty apps or more. How does Django differentiate the URL names between them? For example,
the polls app has a detail view, and so might an app on the same project that is for a blog.
How does one make it so that Django knows which app view to create for a url when using
the `{% url %}` template tag?

The answer is to add namespaces to your URLconf.
In the polls/urls.py file, go ahead and add an app_name to set the application namespace:
polls/urls.py¶