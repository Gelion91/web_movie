#!/bin/sh
source env/bin/activate
celery -A tasks worker -B --loglevel=INFO
