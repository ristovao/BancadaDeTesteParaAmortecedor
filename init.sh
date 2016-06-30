find ./ -name "migrations" | xargs rm -rf
rm db.sqlite3
python manage.py makemigrations app
python manage.py migrate
python manage.py createsuperuser
