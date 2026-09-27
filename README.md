# 📰 Blog Project With Django

<!-- <p align = "center">
  <img src = "https://github.com/zumrudu-anka/Blog-Project-With-Django/blob/master/presentationMedia/1.gif">
  <img src = "https://github.com/zumrudu-anka/Blog-Project-With-Django/blob/master/presentationMedia/2.gif">
  <img src = "https://github.com/zumrudu-anka/Blog-Project-With-Django/blob/master/presentationMedia/3.gif">
  <img src = "https://github.com/zumrudu-anka/Blog-Project-With-Django/blob/master/presentationMedia/4.gif">
</p> -->

## Installation

- Clone the repo to your local machine `git clone https://github.com/zumrudu-anka/django-blog-project.git`
- Go to the project folder
- run `python -m venv myvenv` for create virtual environment which name is myvenv
- run `pip install -r requirements`
- Secret Key:  
> For Windows:
> - create env.bat file in the project directory
> - write `set SECRET_KEY=yoursecretkey` to this file
> - run `env.bat`

> For Linux:
> - create .env file in the project directory
> - write `SECRET_KEY=yoursecretkey` to this file
> - run `source .env`

> You can create new secret key:
> - run python manage.py shell and write this lines
> - from django.core.management.utils import get_random_secret_key
> - print(get_random_secret_key()) # copy the result and write to your env file.
> - exit() # to exit the shell.

- run `python manage.py makemigrations`
- run `python manage.py migrate`

## Usage

- run `python manage.py runserver`

## Deployment

- Set `SECRET_KEY` and `DJANGO_DEBUG=False` as environment variables (the app refuses to start without a `SECRET_KEY` when debug is off)
- run `python manage.py migrate` (also creates the cache table used by the rate limiter in `blog/ratelimit.py`)
- On Coolify, Nixpacks' default start command already runs `migrate` on every start; create an admin once with `python manage.py createsuperuser`
- run `python manage.py collectstatic --noinput`
- The app rate-limits login, sign-up, comments and new articles, but real DDoS protection has to happen in front of Django (e.g. Cloudflare or nginx `limit_req`)
- Serve with `gunicorn blog.wsgi` behind an HTTPS proxy; user uploads in `media/` must be served by the web server when `DEBUG` is off

## Source

[Mustafa Murat Coşkun - Sıfırdan İleri Seviyeye Python Kursu](https://www.udemy.com/course/sifirdan-ileri-seviyeye-python/)
