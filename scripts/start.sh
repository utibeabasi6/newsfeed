#!/bin/sh
cd /home/ubuntu/newsfeed/ && gunicorn --bind 0.0.0.0:5000 main:app -D