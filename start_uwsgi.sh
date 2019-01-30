#!/bin/bash

PROJECT_PATH="$(pwd)"

# Official Django configuration
pipenv run uwsgi --chdir=$PROJECT_PATH \
	--module=med.wsgi:application \
	--env DJANGO_SETTINGS_MODULE=med.settings \
	--master --pidfile=$PROJECT_PATH/uwsgi.pid \
	--socket=$PROJECT_PATH/uwsgi.sock \
	--processes=5 \
	--chmod-socket=600 \
	--harakiri=20 \
	--max-requests=5000 \
	--vacuum \
	--daemonize=$PROJECT_PATH/uwsgi.log \
	--protocol=fastcgi

