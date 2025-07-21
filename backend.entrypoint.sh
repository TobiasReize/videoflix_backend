#!/bin/sh

set -e

echo "Warte auf PostgreSQL auf $DB_HOST:$DB_PORT..."

# -q für "quiet" (keine Ausgabe außer Fehlern)
# Die Schleife läuft, solange pg_isready *nicht* erfolgreich ist (Exit-Code != 0)
while ! pg_isready -h "$DB_HOST" -p "$DB_PORT" -q; do
  echo "PostgreSQL ist nicht erreichbar - schlafe 1 Sekunde"
  sleep 1
done

echo "PostgreSQL ist bereit - fahre fort..."

# Deine originalen Befehle (ohne wait_for_db)
python manage.py collectstatic --noinput
python manage.py makemigrations
python manage.py migrate

# Disable user mails
export DISABLE_USER_MAIL=true

# Create a superuser using environment variables
# (Dein Superuser-Erstellungs-Code bleibt gleich)
python manage.py shell <<EOF
import os
from django.contrib.auth import get_user_model

User = get_user_model()
username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'adminpassword')
confirmed = os.environ.get('CONFIRMED', False)

if not User.objects.filter(username=username).exists():
    print(f"Creating superuser '{username}'...")
    User.objects.create_superuser(username=username, email=email, password=password, confirmed=confirmed)
    print(f"Superuser '{username}' created.")
else:
    print(f"Superuser '{username}' already exists.")

# Gast-User erstellen, falls nicht vorhanden
username_guest = os.environ.get('GUEST_USERNAME', 'Guest')
email_guest = os.environ.get('GUEST_EMAIL', 'guest@example.de')
password_guest = os.environ.get('GUEST_PASSWORD', 'password')

if not User.objects.filter(email=email_guest).exists():
    print("Creating guest user...")
    User.objects.create_user(username=username_guest, email=email_guest, password=password_guest, confirmed=confirmed)
    print(f"Guest user created.")
else:
    print("Guest user already exists.")
EOF

# Reactivate user emails
unset DISABLE_USER_MAIL

python manage.py rqworker default &

exec gunicorn videoflix_backend.wsgi:application \
  --bind 0.0.0.0:8000 \
  --workers 3 \
  --log-level info \
  --access-logfile - \
  --error-logfile -
