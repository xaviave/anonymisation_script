#!/usr/bin/env bash

python3 manage.py migrate --run-syncd
python3 manage.py runserver 0.0.0.0:8000