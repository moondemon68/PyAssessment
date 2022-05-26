#!/bin/bash
exec gunicorn --config gunicorn_config.py web_service.src.wsgi:app