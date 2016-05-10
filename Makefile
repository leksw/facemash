manage=python manage.py
APP_LIST ?= core facemash


flake8=flake8 --max-complexity=7


start_db:
	sudo service postgresql start

stop_db:
	sudo service postgresql stop

run:
	PYTHONPATH=$(PYTHONPATH) $(manage) runserver $(IP):$(PORT)

test:
	$(flake8) --exclude=migrations,settings.py --max-complexity=8 $(APP_LIST)
	PYTHONPATH=$(PYTHONPATH) $(manage) test -v2

coverage_test:
	@coverage run --source=. manage.py test -v2 $(APP_LIST)

install:
	pip install -r requirements/dev.txt

migrate:
	PYTHONPATH=$(PYTHONPATH) $(manage) migrate

mkmigrate:
	PYTHONPATH=$(PYTHONPATH) $(manage) makemigrations