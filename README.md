# movie-app
## how to run ?
1. Go to _requirements.txt_ file and create environment
### Linux
2. To run the batch file using the call command, enter the following command:
> bash build.sh

### windows
2. To run the batch file using the call command, enter the following command:
> call build.bat

### Docker
- If you have Docker and docker-compose installed, you can just run:
> docker-compose up --build

### Create a superuser
3. Create a _superuser_ account 
> python manage.py createsuperuser

### Run the Web Server
4. Run python development Server
> python manage.py runserver

### Admin Account
- To login into admin go to 127.0.0.1:8000/admin/

## Additonal Info
For OMDB_API_KEY visit https://www.omdbapi.com/ and request an API key(for search function)

