@echo off

REM Apply database migrations
python manage.py migrate

REM Collect static files
python manage.py collectstatic --noinput

REM add data to database
python manage.py runscript data_filler -v3

echo Build completed successfully!
