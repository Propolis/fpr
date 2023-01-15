# http://gagai-foodgram.webhop.me

# Foodgram - это сервис для публикации ваших рецептов.
##### Здесь вы можете создать свои рецепты и просматривать рецепты других пользователей.

##### В проекте реализованы:
 * пользовательские подписки
 * добавление и удаление рецептов в избранное и список покупок
 * фильтрация рецептов по тегам
 * настройка админ панели Django

##### Полную спецификацию по проекту можно посмотреть здесь:
* http://gagai-foodgram.webhop.me/api/docs/

##### Проект разворачивается в четырёх Docker контейнерах:
* foodgram-frontend: отвечает за сборку фронтенда
* foodgram-backend: реализация всей логики сервиса
* postgresql: настраивает работу БД PostgreSQL
* nginx: прописана настройка серверной части проекта

##### Запуск проекта:
Скопируйте репозиторий
```
git@github.com:gagai/foodgram-project-react.git
```

Перейдите в папку развертывания инфраструктуры проекта 
и создайте файл с переменными окружения **.env**
```
cd foodgram-project-react/infra/
nano .env
```
Файл .env заполняется следующим образом:

SECRET_KEY=django-insecure-$9*$q+7jq5^%kp#$1+y+r-h0$d9_$+y4a6n5)h67o(v&bk_#r+
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
DB_USER=postgres
POSTGRES_PASSWORD=postgres **(установите свой)**
DB_HOST=postgresql
DB_PORT=5432

Убедитесь, что у вас свободны порты 8000 и 5432.
После запуска docker-compose создайте миграции, соберите статику,
загрузите в базу данных теги и ингредиенты и создайте суперпользователя
```
docker-compose up -d
docker-compose exec backend python3 manage.py makemigrations
docker-compose exec backend python3 manage.py migrate
docker-compose exec backend python3 manage.py collectstatic --no-input
docker-compose exec backend python3 manage.py load_test_data
docker-compose exec backend python3 manage.py createsuperuser
```

Готово!
Проект можно открыть по адресу http://localhost/
Управлять проектом можно по адресу http://localhost/admin/
