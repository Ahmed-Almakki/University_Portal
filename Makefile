make_mig:
	python manage.py makemigrations

mig:
	python manage.py migrate

run:
	python manage.py runserver