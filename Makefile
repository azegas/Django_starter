.PHONY: mm m run freeze super pre pre-all

m:
	python manage.py migrate

mm:
	python manage.py makemigrations

run:
	python manage.py runserver

freeze:
	pip freeze > requirements.txt

super:
	python manage.py createsuperuser
