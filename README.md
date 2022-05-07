# Описание
Проект **YaMDb** собирает отзывы пользователей на различные произведения.

#### Алгоритм регистрации пользователей
1. Пользователь отправляет POST-запрос на добавление нового пользователя с параметрами `email` и `username` на эндпоинт `/api/v1/auth/signup/`.
2. **YaMDB** отправляет письмо с кодом подтверждения (`confirmation_code`) на адрес  `email`.
3. Пользователь отправляет POST-запрос с параметрами `username` и `confirmation_code` на эндпоинт `/api/v1/auth/token/`, в ответе на запрос ему приходит `token` (JWT-токен).
4. При желании пользователь отправляет PATCH-запрос на эндпоинт `/api/v1/users/me/` и заполняет поля в своём профайле (описание полей — в документации).

#### Пользовательские роли
- **Аноним** — может просматривать описания произведений, читать отзывы и комментарии.
- **Аутентифицированный пользователь** (`user`) — может, как и **Аноним**, читать всё, дополнительно он может публиковать отзывы и ставить оценку произведениям (фильмам/книгам/песенкам), может комментировать чужие отзывы; может редактировать и удалять **свои** отзывы и комментарии. Эта роль присваивается по умолчанию каждому новому пользователю.
- **Модератор** (`moderator`) — те же права, что и у **Аутентифицированного пользователя** плюс право удалять **любые** отзывы и комментарии.
- **Администратор** (`admin`) — полные права на управление всем контентом проекта. Может создавать и удалять произведения, категории и жанры. Может назначать роли пользователям. 
- **Суперюзер Django** — обладет правами администратора (`admin`)


#### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/.../api_yamdb
cd api_yamdb
```

#### Шаблон наполнения ENV файла:

ENV файл с переменными окружения имеет вид:

SECRET_KEY==........... # указывать секретный код
DB_ENGINE=........... # тут необходимо указывать, что работаем с postgresql
DB_NAME=........... # указываем имя базы данных
POSTGRES_USER=........... # логин для подключения к базе данных
POSTGRES_PASSWORD=........... # указать пароль для подключения к БД (установите свой)
DB_HOST==........... # название сервиса (контейнера)
DB_PORT==........... # порт для подключения к БД


#### Команды для запуска приложения в контейнерах:

1. После заполнения Dockerfile, оставаясь в одной с ним директории, запускаем сборку образа командой:
docker build -t (укажите название образа тут) . (точка обязательна - указывает путь до Dockerfile)

2. Далее, следующей командой вызывает сборку и запуск контейнера
docker run --name (укажите название контейнера тут) -it -p 8000:8000 yamdb

Данные команды подходят для сбора самого простого приложения. Но так как проект api_yamdb работает
на базе данных, полезней создать несколько контейнеров для каждого сервиса. А несколько котейнеров 
взаимодействуют через утилиту docker-compose.

#### Настройки Базы данных проекта примут вид:

DATABASES = {
    'default': {
        'ENGINE': os.getenv('DB_ENGINE'),
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('POSTGRES_USER'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT')
    }
}

После подготовки файла docker-compose (включая контейнер nginx), поднять проект с 
имеющейся базой данных можно одной командой:

1. docker-compose up -d --build

Далее необходимо выполнить миграции и создать суперпользователя 
(команды выполняются поочередно, одна за другой):

1. docker-compose exec web python manage.py migrate
2. docker-compose exec web python manage.py createsuperuser
3. docker-compose exec web python manage.py collectstatic --no-input

Проект будет доступен по ссылке http://localhost/admin/

Остановить работу контейнеров можно командой 

1. docker-compose down -v