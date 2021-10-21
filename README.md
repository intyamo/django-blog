# Plan

## Initial setup

- create django project

```sh
django-admin startproject config .
```

- apply initial migrations

```sh
python manage.py migrate
```

## New App

- create new app

```sh
python manage.py startapp <appname>
```

- register app in django settings

`config/settings.py`

```py
INSTALLED_APPS = [
                 # ...
                 < appname >,
]
```

## Database Models

- design models

`<appname>/models.py`

- apply db migrations of new models

```sh
python manage.py makemigrations <appname>
python manage.py migrate <appname>
```

## Admin

- create superuser

```sh
python manage.py createsuperuser
```

- register app models within app admin

`<appname>/admin.py`

```py
from .models import < model >  # etc

admin.site.register( < model >)
```

## URLs -> Views -> Templates

### URLs

`<appname>/urls.py`

```py
from django.urls import path

# these views will be created on the next step
from .views import MyView1, MyView2

urlpatterns = [
    path('', MyView1.as_view(), name='home'),
    path('something/<int:pk>/', MyView2.as_view(),
         name='something_details'),
]
```

- include in project's URLs

`config/urls.py`

```py
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # ...
    path('', include('<appname>.urls')),
]
```

### Views

`<appname>/views.py`

```py
from django.views.generic import ListView  # etc

# import our models to be used as data sources for views
from .models import MyEntity  # etc


class AppEntityListView(ListView):
    model = MyEntity
    template_name = 'home.html'
    paginate_by = 5
    page_kwarg = "my_entity_name"


class AppEntityDetailsView(ListView):
    model = MyEntity
    template_name = '<entity>_details.html'


class AppEntityCreateView():
    model = MyEntity
    template_name = '<entity>_create.html'
    # fields - actual attributes of MyEntity
    fields = ['field_1', 'field_2', 'field_3']
```

### Templates

Let's store templates in `<project_root>/templates`

```sh
mkdir templates

touch templates/base.html
touch templates/home.html
touch templates/entity_details.html
# ...
```

Update templates directory in `config/settings.py`:

```py
TEMPLATES = {
    # ...
    "DIRS": [str(BASE_DIR / "templates")],
    # ...
}
```

# Deployment to Heroku

0. Register on [Heroku](https://signup.heroku.com/)
1. Install [`heroku-cli`](https://devcenter.heroku.com/articles/heroku-cli)
2. Create an app

```shell
heroku create --region eu
```

You'll get a remote repository named `heroku` added to your git repo, handy!

3. Add required dependencies

```shell
pipenv install gunicorn dj-database-url psycopg2-binary
```

4. Add [`Procfile`](https://devcenter.heroku.com/articles/procfile)

Sample `./Procfile`:

```shell
web: gunicorn config.wsgi --log-file -
```

6. Setup environment on Heroku

- generate secret key to use in production:

```shell
python manage.py shell -c 'from django.core.management import utils; print(utils.get_random_secret_key())'
```

- set it up on Heroku:

```shell
heroku config:set DJANGO_SECRET_KEY=<key_generated_above>
```

- turn off debug mode:

```shell
heroku config:set DJANGO_DEBUG=False
```

7. Check Django settings (`config/settings.py`)

These settings should respect environment:

- `SECRET_KEY` - `DJANGO_SECRET_KEY`
- `DATABASES` - `DATABASE_URL`
- `DEBUG` - `DJANGO_DEBUG`

`ALLOWED_HOSTS` should include Heroku, i.e.:

```python
ALLOWED_HOSTS = [".herokuapp.com", "localhost", "127.0.0.1"]
```

Refer to [`4897e92`](https://github.com/intyamo/django-blog/commit/4897e92f2eb6a5e45433577043a66cc9183035b3) if needed.

8. Push to Heroku!

```shell
git push heroku master
```

8. Start your web app and check its logs!

```shell
heroku ps:scale web=1

# logs
heroku logs --tail      
```
