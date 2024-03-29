#!/bin/sh
python3 manage.py migrate
python3 manage.py fill_location_data
python3 manage.py fill_cars
python3 manage.py runserver