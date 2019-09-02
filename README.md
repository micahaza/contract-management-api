# Simple Contract Management API

## Workflow I'm implementing here
......

# Setup guide

## Prerequisites
* python3, mysql server

## Setup virtual environment
* python3 -m virtualenv env
* source ./env/bin/activate

## Install required library
* pip install pip --upgrade
* pip install -r requirements.txt

## Configuring the app
You have to create a folder called instance in the project root. Create two files, development.cfg, testing.cfg
/jcapi
/instance
  development.cfg
  testing.cfg

Example content of these files (development.cfg):
```
DEBUG = True
SQLALCHEMY_DATABASE_URI = 'mysql://<user>:<password>@localhost/<database_name>'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = '2s-ymN5--KIp7goh-CVRrliS9aMTrYuVmWy3-CYnXjJcq3AZXHLBOf8I26aw_5AHUf7'
JWT_SECRET_KEY = '1ZNA-ax-6NW-J8VR7hsRxNvfvoMm5mahcYTO6RGra-nVv8AArsWlc10xcLN4Ha1I-XdcoYpL'
JWT_ACCESS_TOKEN_EXPIRES = 1800

MAIL_SERVER='your server address'
MAIL_PORT=465
MAIL_USERNAME='login@blockspire.com'
MAIL_PASSWORD='my pass'
MAIL_DEFAULT_SENDER='deezent@blockspire.com'
MAIL_ENABLED=True
```

I'm generating these secret keys like this:

```
bash$ < /dev/urandom tr -dc _A-Z-a-z-0-9 | head -c${1:-64};echo;
```

## Database install && migrate
* mysql> CREATE DATABASE jc_dev;
* mysql> CREATE DATABASE jc_test;
* export FLASK_APP=run.py
* flask db init
* flask db migrate
* flask db upgrade

## Run tests

### You can run it with tox
* tox

### Or manually
* export FLASK_ENV=development
* export FLASK_APP=run.py
* py.test -v

### Run the app
* ./start.sh