# movie-app
## how to run ?
### Linux
1. Execute virtual environment
> python -m venv .venv

2. Enter in virtual environment
> source .venv/bin/execute

- For windows, [How To Set Up a Virtual Python Environment](https://mothergeo-py.readthedocs.io/en/latest/development/how-to/venv-win.html)

3. Install requirements
> pip install -r requirements.txt

4. Run Django development server
> python manage.py runserver  

- If you have Docker and docker-compose installed, you can just run:
> docker-compose up --build

## Additonal Info
For OMDB_API_KEY visit https://www.omdbapi.com/ and request an API key(for search function)
