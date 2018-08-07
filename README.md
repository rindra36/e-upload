# E-UPLOAD
Research project using Django with PostgreSQL database.

## Getting started
It has been developed using Antergos OS. So all commands for installation come from Arch Linux.

### Prerequisites
First install python, pip, django, postgresql
```
sudo pacman -S python python-pip python-django postgresql
```
Create schema in your PostgreSQL database
```
sudo su - postgres
psql
CREATE DATABASE yourprojectdatabasename;
CREATE USER username WITH PASSWORD password;
GRANT ALL PRIVILEGES ON DATABASE yourprojectdatabasename TO username;
\q
exit
```
Install [Stronghold](https://github.com/mgrouchy/django-stronghold) and [Python-PostgreSQL Database Adapter](https://github.com/psycopg/psycopg2)
```
sudo pip install psycopg2 django-stronghold
```

### Installation
After installing prerequisites and cloning the repository, edit `eboutique/settings.py` in DATABASES section:
```python
. . .
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'yourprojectdatabasename',
        'USER': 'username',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '',
    }
}
. . .
```
run in terminal
```
python manage.py makemigrations
```
Then
```
python manage.py migrate
```
to create tables in the schema.

After creating database structure, we can create an administrative account by typing:
```
python manage.py createsuperuser
```
You will be asked to select a username, provide an email address, and choose and confirm a password for the account.

Once an admin account was created, run in the terminal:
```
python manage.py runserver
```
and go to
```
http://server_domain_IP:8000/login
```
### Credits
* [Semantic-UI](http://semantic-ui.com/)
* [FancyBox](https://fancyapps.com/fancybox/3/)
* [Glide.js](https://glidejs.com/)
* [Login-template](https://colorlib.com/wp/template/login-form-v17/)
