# Videoflix Backend

## A Django-based backend project for a video streaming platform.<br/>
Videoflix uses Django and Django Restframework (DRF) to provide individual endpoints, authentication and permissions. PostgreSQL as database and Redis for Caching-Layer. FFmpeg including Django-RQ is used to convert the videos.

This project is part of the videoflix_frontend.<br/>

## Prerequisites:
`Python version >= 3.10`

## How to install this repository on a Linux server or WSL:

1. Clone this repository:
```
    git clone <GitHub repository link>
```

2. Create a virtual environment (in the project folder):
```
    python3 -m venv env_lin
```

3. Install the dependencies:
```
    activate the virtual environment: source env_lin/bin/activate
    pip install -r requirements.txt
```

4. Install packages:
```
    sudo apt-get install ffmpeg
    sudo apt-get install redis
    sudo apt install postgresql postgresql-contrib
```
(--> edit password in redis.conf)</br>
(--> set up postgres database)

5. Set the environment variables:
```
    rename the .env-template file to .env and fill out the environment variables
```

6. Run background processes:
```
    sudo service redis-server start
    sudo service postgresql start
    python manage.py rqworker
```

7. Apply migrations:
```
    python manage.py makemigrations
    python manage.py migrate
```

8. Create a Superuser/ Admin: (only superuser can add videos)
```
    python manage.py createsuperuser
```

9. Create static files:
```
    python manage.py collectstatic
```

10. Run the local development server (on path: 127.0.0.1:8000):
```
    python manage.py runserver
```

11. Start videoflix_frontend:<br/>
clone the repository and run the liveserver on path 127.0.0.1:4200
