# 📰 Blog Project With Django

<p align = "center">
  <img src = "https://github.com/zumrudu-anka/Blog-Project-With-Django/blob/master/presentationMedia/1.gif">
  <img src = "https://github.com/zumrudu-anka/Blog-Project-With-Django/blob/master/presentationMedia/2.gif">
  <img src = "https://github.com/zumrudu-anka/Blog-Project-With-Django/blob/master/presentationMedia/3.gif">
  <img src = "https://github.com/zumrudu-anka/Blog-Project-With-Django/blob/master/presentationMedia/4.gif">
</p>

### Installation

- Clone this repo to your local machine using `https://github.com/zumrudu-anka/django-blog-project.git`
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

### Usage

- run `python manage.py runserver`
