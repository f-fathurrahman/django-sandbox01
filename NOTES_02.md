Database setup

Now, open up mysite/settings.py. It’s a normal Python module with module-level variables representing Django settings.

By default, the configuration uses SQLite. If you’re new to databases, or you’re just interested in trying Django, this is the easiest choice. SQLite is included in Python, so you won’t need to install anything else to support your database. When starting your first real project, however, you may want to use a more scalable database like PostgreSQL, to avoid database-switching headaches down the road.

If you wish to use another database, install the appropriate database bindings and change the following keys in the DATABASES 'default' item to match your database connection settings:

    ENGINE – Either 'django.db.backends.sqlite3', 'django.db.backends.postgresql', 'django.db.backends.mysql', or 'django.db.backends.oracle'. Other backends are also available.
    NAME – The name of your database. If you’re using SQLite, the database will be a file on your computer; in that case, NAME should be the full absolute path, including filename, of that file. The default value, BASE_DIR / 'db.sqlite3', will store the file in your project directory.

If you are not using SQLite as your database, additional settings such as USER, PASSWORD, and HOST must be added. For more details, see the reference documentation for DATABASES.






# Creating models

Now we’ll define your models – essentially, your database layout, with additional metadata.



Philosophy

A model is the single, definitive source of information about your data. It contains the 
essential fields and behaviors of the data you’re storing. Django follows the DRY Principle. 
The goal is to define your data model in one place and automatically derive things from it.

This includes the migrations - unlike in Ruby On Rails, for example, migrations are entirely 
derived from your models file, and are essentially a history that Django can roll through to 
update your database schema to match your current models.

In our poll app, we’ll create two models: Question and Choice. A Question has a question and a publication date. A Choice has two fields: the text of the choice and a vote tally. Each Choice is associated with a Question.

These concepts are represented by Python classes. Edit the polls/models.py file so it looks like this:

File polls/models.py
```python
from django.db import models


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
```

Here, each model is represented by a class that subclasses django.db.models.Model.
Each model has a number of class variables, each of which represents a database field in the model.

Each field is represented by an instance of a Field class – e.g., CharField for character fields and 
DateTimeField for datetimes. This tells Django what type of data each field holds.

The name of each Field instance (e.g. question_text or pub_date) is the field’s name, in machine-friendly format. 
You’ll use this value in your Python code, and your database will use it as the column name.

You can use an optional first positional argument to a Field to designate a human-readable name. That’s used in a 
couple of introspective parts of Django, and it doubles as documentation. If this field isn’t provided, Django 
will use the machine-readable name. In this example, we’ve only defined a human-readable name for Question.
pub_date. For all other fields in this model, the field’s machine-readable name will suffice as its 
human-readable name.

Some Field classes have required arguments. CharField, for example, requires that you give it a max_length. 
That’s used not only in the database schema, but in validation, as we’ll soon see.

A Field can also have various optional arguments; in this case, we’ve set the default value of votes to 0.

Finally, note a relationship is defined, using ForeignKey. That tells Django each Choice is related to a single 
Question. Django supports all the common database relationships: many-to-one, many-to-many, and one-to-one.


# Activating models

That small bit of model code gives Django a lot of information. With it, Django is able to:

- Create a database schema (CREATE TABLE statements) for this app.

- Create a Python database-access API for accessing Question and Choice objects.

But first we need to tell our project that the polls app is installed.

To include the app in our project, we need to add a reference to its configuration class in
the INSTALLED_APPS setting. The PollsConfig class is in the polls/apps.py file,
so its dotted path is 'polls.apps.PollsConfig'.
Edit the mysite/settings.py file and add that dotted path to the INSTALLED_APPS setting. It’ll look like this:

File: mysite/settings.py
```python
INSTALLED_APPS = [
    "polls.apps.PollsConfig",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]
```

Now Django knows to include the polls app. Let’s run another command:
```
python manage.py makemigrations polls
```

You should see something similar to the following:
```
Migrations for 'polls':
  polls/migrations/0001_initial.py
    - Create model Question
    - Create model Choice
```

By running makemigrations, you’re telling Django that you’ve made some changes to your models (in this case, 
you’ve made new ones) and that you’d like the changes to be stored as a migration.

Migrations are how Django stores changes to your models (and thus your database schema) - they’re files on disk. 
You can read the migration for your new model if you like; it’s the file polls/migrations/0001_initial.py. Don’t 
worry, you’re not expected to read them every time Django makes one, but they’re designed to be human-editable in 
case you want to manually tweak how Django changes things.

There’s a command that will run the migrations for you and manage your database schema automatically - that’s 
called migrate, and we’ll come to it in a moment - but first, let’s see what SQL that migration would run. The 
sqlmigrate command takes migration names and returns their SQL:
```
python manage.py sqlmigrate polls 0001
```

You should see something similar to the following (we’ve reformatted it for readability):
```sql
BEGIN;
--
-- Create model Question
--
CREATE TABLE "polls_question" (
    "id" bigint NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    "question_text" varchar(200) NOT NULL,
    "pub_date" timestamp with time zone NOT NULL
);
--
-- Create model Choice
--
CREATE TABLE "polls_choice" (
    "id" bigint NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    "choice_text" varchar(200) NOT NULL,
    "votes" integer NOT NULL,
    "question_id" bigint NOT NULL
);
ALTER TABLE "polls_choice"
  ADD CONSTRAINT "polls_choice_question_id_c5b4b260_fk_polls_question_id"
    FOREIGN KEY ("question_id")
    REFERENCES "polls_question" ("id")
    DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX "polls_choice_question_id_c5b4b260" ON "polls_choice" ("question_id");

COMMIT;
```

Note the following:

- The exact output will vary depending on the database you are using. The example above is generated for PostgreSQL.

- Table names are automatically generated by combining the name of the app (polls) and the lowercase name of the model – question and choice. (You can override this behavior.)

- Primary keys (IDs) are added automatically. (You can override this, too.)

- By convention, Django appends "_id" to the foreign key field name. (Yes, you can override this, as well.)
  The foreign key relationship is made explicit by a FOREIGN KEY constraint. Don’t worry about the DEFERRABLE parts; it’s telling PostgreSQL to not enforce the foreign key until the end of the transaction.
  It’s tailored to the database you’re using, so database-specific field types such as auto_increment (MySQL), 
  bigint PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY (PostgreSQL), or integer primary key autoincrement (SQLite) 
  are handled for you automatically. Same goes for the quoting of field names – e.g., using double quotes or 
  single quotes.
  
The sqlmigrate command doesn’t actually run the migration on your database - instead,
it prints it to the screen so that you can see what SQL Django thinks is required.
It’s useful for checking what Django is going to do or if you have database
administrators who require SQL scripts for changes.

If you’re interested, you can also run python manage.py check; this checks for any problems in your project 
without making migrations or touching the database.

Now, run migrate again to create those model tables in your database:

The migrate command takes all the migrations that haven’t been applied (Django tracks which ones are applied using a special table in your database called django_migrations) and runs them against your database - essentially, synchronizing the changes you made to your models with the schema in the database.

Migrations are very powerful and let you change your models over time, as you develop your project, without the need to delete your database or tables and make new ones - it specializes in upgrading your database live, without losing data. We’ll cover them in more depth in a later part of the tutorial, but for now, remember the three-step guide to making model changes:

- Change your models (in models.py).

- Run python manage.py makemigrations to create migrations for those changes

- Run python manage.py migrate to apply those changes to the database.

The reason that there are separate commands to make and apply migrations is because you’ll commit migrations to your version control system and ship them with your app; they not only make your development easier, they’re also usable by other developers and in production.

Read the django-admin documentation for full information on what the manage.py utility can do.


