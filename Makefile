# инициализировать виртуальную машину
up:
	vagrant up

# установить зависимости проекта
install:
	vagrant ssh -c "cd /vagrant/ && poetry install"

# сделать дата-миграции бд
migrate:
	vagrant ssh -c "cd /vagrant/etl && poetry run python manage.py makemigrations && poetry run python manage.py migrate"

# запустить сервер разработки
runserver:
	vagrant ssh -c "cd /vagrant/etl && poetry run python manage.py runserver 0.0.0.0:8000"
