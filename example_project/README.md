# Running the med website

We assume that you are using Debian Stretch or Buster and that django-library is
installed via pip in your Python 3 environment.

Clone the project (can be in `/var/local`):

```bash
$ git clone https://github.com/erdnaxe/django-library.git
$ cd django-library/example_project
```

Now we need to create the database tables and an admin user.
Run the following and when prompted to create a
superuser choose yes and follow the instructions:

```bash
$ python3 manage.py migrate
$ python3 manage.py createsuperuser
```

Now you need to run the Django development server:

```
$ python3 manage.py runserver
```

You should then be able to open your browser on <http://127.0.0.1:8000> and see
django-library running.

## For a production environment

You should use PostgreSQL (`psycopg2` and `postgresql` packages)
or MySQL (`python3-mysqldb`, `mysql-client` and `mysql-server` packages).

For MySQL, use the following to create a database:

```SQL
CREATE DATABASE library;
CREATE USER 'newuser'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON library.* TO 'newuser'@'localhost';
FLUSH PRIVILEGES;
```
