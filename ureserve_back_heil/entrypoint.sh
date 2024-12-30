#!/bin/bash

set -e

if [$1 == 'gunicorn']; then

    exec gunicorn ReserveProject.wsgi:application -b 0.0.0.0:4001

else

    exec python3 manage.py runserver 0.0.0.0:8000

fi