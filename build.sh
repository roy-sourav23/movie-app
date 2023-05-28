#!/bin/bash

# Apply database migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Add data to the database
python manage.py runscript data_filler -v3

echo "Build completed successfully!"
