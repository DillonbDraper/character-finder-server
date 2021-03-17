#!/bin/bash
git rm -rf --cached db.sqlite3   
rm -rf rareapi/migrations
rm db.sqlite3
python3 manage.py migrate
python3 manage.py makemigrations character_finder_api
python3 manage.py migrate character_finder_api
python3 manage.py loaddata users
python3 manage.py loaddata tokens
python3 manage.py loaddata genres
python3 manage.py loaddata series
python3 manage.py loaddata readers
python3 manage.py loaddata authors
python3 manage.py loaddata fictions
python3 manage.py loaddata characters
python3 manage.py loaddata character_associations
python3 manage.py loaddata author_fictions
python3 manage.py loaddata fiction_characters
