find ./ -name "migrations" | xargs rm -rf
rm db.sqlite3
python3.5 manage.py makemigrations app
python3.5 manage.py migrate
python3.5 manage.py createsuperuser
