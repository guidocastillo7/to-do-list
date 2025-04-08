#!/usr/bin/env bash

set -o errexit

pip install -r requirements.txt

python todolist/manage.py collectstatic --no-input