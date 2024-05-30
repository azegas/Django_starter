## TESTS ##

.PHONY: test coverage
test:
	python manage.py test

# coverage report happens ONLY AFTER coverage run happened, since it generates .coverage file needed for the report
coverage:
	coverage run manage.py test & coverage report > coverage.txt

##DJANGO STUFF ##

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
