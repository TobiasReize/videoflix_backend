# Videoflix Backend

## A Django-based backend project for a video streaming platform.<br/>
Videoflix uses Django and Django Restframework (DRF) to provide individual endpoints, authentication and permissions. PostgreSQL as database and Redis for Caching-Layer. FFmpeg including Django-RQ is used to convert the videos.

This project is part of the videoflix_frontend.<br/>


## How to install this repository on a Linux server:

1. Clone this repository:
```
    git clone <GitHub repository link>
```

2. Create a virtual environment (in the project folder):
```
    python -m venv env_lin
```

3. Install the dependencies:
```
    activate the virtual environment
    pip install -r requirements.txt
```

4. Set the environment variables:
```
    rename the .env-template file to .env and fill out the environment variables
```

5. Apply migrations:
```
    python manage.py makemigrations
    python manage.py migrate
```

6. Create a Superuser/ Admin:
```
    python manage.py createsuperuser
```

7. Create static files:
```
    python manage.py collectstatic
```

8. Run the local development server (on path: 127.0.0.1:8000):
```
    python manage.py runserver
```

9. Run background processes:
```
    sudo service redis-server start
    python manage.py rqworker
```

10. Start videoflix_frontend:<br/>
clone the repository and run the liveserver on path 127.0.0.1:4200
