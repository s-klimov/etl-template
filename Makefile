# инициализация виртуальной машины
up:
	vagrant up

# миграции бд
migrate:
	vagrant ssh -c "cd /vagrant/ && poetry run python manage.py migrate"

# запуск сервера разработки
runserver:
	vagrant ssh -c "cd /vagrant/ && poetry run python manage.py runserver 0.0.0.0:8181"
