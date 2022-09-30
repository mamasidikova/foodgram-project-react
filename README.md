# CI/CD для проекта Foodgram

[![Django-app workflow](https://github.com/DeffronMax/foodgram-project-react/actions/workflows/main.yml/badge.svg)](https://github.com/DeffronMax/foodgram-project-react/actions/workflows/main.yml)

# Foodgram
Это сервис, где вы можете создавать свои собственные рецепты, подписываться на других пользователей, добавлять рецепты в избранное, добавлять рецепты в корзину и скачивать список ингредиентов с их количеством.

## Установка зависимостей
Для установки компонентов у вас должна быть машина на linux и docker [docker](https://www.docker.com/).

[HOWTO](https://docs.docker.com/engine/install/) for installing docker.

После установки docker включите сервис и добавьте его в автозапуск.

```bash
sudo systemctl enable docker && sudo systemctl restart docker
```

## Установка Foodgram

Для установки Foodgram необходимо перейти по ссылке [github link](git@github.com:mamasidikova/foodgram-project-react.git), и запустить команды ниже.

Если у вас нет гитхаба [github](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) на рабочей машине, требуется его установить.

```bash
git clone git@github.com:mamasidikova/foodgram-project-react.git

cd foodgram-project-react/infra

sudo docker-compose up -d --build
```

## Database form

После установки следует сделать миграции для базы данных, создать суперпользователя и собрать статику.

```bash
sudo docker-compose exec web python3 manage.py makemigrations recipes --noinput

sudo docker-compose exec web python3 manage.py migrate --noinput

sudo docker-compose exec web python3 manage.py createsuperuser

sudo docker-compose exec web python3 manage.py collectstatic --no-input
```

## Завершение установки

Проект имеет готовую базу ингредиентов.

Чтобы добавить контент в свою базу данных, вы можете запустить команду ниже:

```bash
sudo docker-compose exec web python3 manage.py load_ingredients data/ingredients.json
```
## Готовый проект

Доступен по адресу: 
```
http://84.201.179.151/
http://84.201.179.151/admin
```
Учётные данные для авторизации в админке:
```
Логин: soche@list.ru
Пароль: elephant
```
