This was set up with [Django](https://www.djangoproject.com/) 1.8.3 on Python 2.7. Everything in Django works with Python 3 but the sample models were set up for Python 2. See the [notes at the bottom](#running-in-python-3) if you want to run it in python 3 instead.

To see the sample project running in the test server:

1. Install [Python 2.7](https://www.python.org/downloads/) (or 3, [see below](#running-in-python-3))

2. Install [Django](https://docs.djangoproject.com/en/1.8/topics/install/#installing-official-release) using pip

3. The sample project also uses an addon that allows markdown formatting for blog posts, so open a command prompt and install [markdown](https://pypi.python.org/pypi/Markdown) and [django-markupfield](https://github.com/jamesturk/django-markupfield) with pip:
   ```
   pip install markdown django-markupfield
   ```

4. In a command prompt, navigate to the django directory and run the development server:
   ```
   python manage.py runserver
   ```

5. Open [http://localhost:8000](http://localhost:8000) in a web browser and you should see the sample site.

That will get everything running in a test server with a sample sqlite database that's included with the code. You should read the [official documentation](https://docs.djangoproject.com/en/1.8/) if you want it to run on a more robust server and database.

## Django Applications and Templates

In the sample project, the homepage hero, homepage features, and blog are all separate ["applications"](https://docs.djangoproject.com/en/1.8/ref/applications/) in the django project. Ideally in a django application, the templates for that application are included in the folder for that application in order to make it portable and self-contained. However, the pattern lab import script has no way of knowing which application something belongs to, and basic patterns should be shared throughout the site anyway, so in this case there is a separate django/templates folder rather than including a templates folder in each application.

## Editing Content

A sqlite database is included with the sample code, so some content is already available when you first run the site as above. If you want to edit the content, go to [http://localhost:8000/admin/](http://localhost:8000/admin/) and log in with the username 'admin' and the password 'password'. That will bring you to the admin dashboard that will allow you to add, edit, or remove the homepage hero and features and the blog posts (as well as users and user groups).

Images are stored in django/images. To add images successfully, the django server will need to be able to write to that folder.

## Editing Data Models

If you make changes to your template that require a change to the data, you will need to edit the data models. Each of the applications (blog, features, and hero) have a models.py file that describes the fields for each data model, and you will add, change, and remove fields there. The [model documentation](https://docs.djangoproject.com/en/1.8/topics/db/models/) describes what you can do there in detail.

After you update the model, you will also need to update the database. Open a command prompt, navigate the the django folder, and run:
```
python manage.py makemigrations appname
python manage.py migrate
```
(where "appname" is the name of the application with the updated model)

## Running in Python 3

Django works in either python 2 or 3, but the sample models were written for python 2. To update for python 3, open blog/models.py, features/models.py and hero/models.py and change 'unicode' to 'str'. E.g.
```
def __unicode__(self):
```
would become
```
def __str__(self):
```
This is really only necessary to display things correctly in the control panel.

## Pagination

Since the converter is shared between several different content management systems, it isn't very well tailored to any of them so the same code can be used across all. In particular, the code for pagination really doesn't make very good use of django's [pagination module](https://docs.djangoproject.com/en/1.8/topics/pagination/). The blog views end up re-implementing pagination themselves instead. If your project has a lot of pagination you may want to customize the import script so you can make better use of the built-in module.