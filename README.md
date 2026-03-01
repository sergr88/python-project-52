# Проект: Менеджер задач (Python)

## Общая информация

### Адрес развертывания:

https://python-project-52-q7xz.onrender.com

### Тесты Hexlet и статус линтера:

[![Actions Status](https://github.com/sergr88/python-project-52/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/sergr88/python-project-52/actions)

## Требования

- uv 0.9+

## Развертывание

- Установите uv

- Перейдите в корневую директорию проекта и выполните
```shell
make build
```

## Проверка кода линтером

```shell
make lint
```

## Исправление ошибок линтером

```shell
make lint-fix
```

## Форматирование кода

```shell
make format
```

## Запуск тестов

```shell
make test
```

## Локализация

- Обновите файлы локализации после изменения строк в шаблонах:
```shell
make makemessages
```

- Заполните файлы локализации в `locale/*/LC_MESSAGES/django.po`

- Скомпилируйте локализацию:
```shell
make compilemessages
```

## Миграции

- Создайте файлы миграций после изменения моделей:
```shell
make makemigrations
```

- Примените миграции:
```shell
make migrate
```

## Интерактивная Django-консоль

```shell
make shell
```

## Создание суперпользователя

По умолчанию суперпользователь отсутствует. Для доступа к админке (`/admin/`)
создайте его вручную:

```shell
uv run manage.py createsuperuser
```

## Запуск сервиса

- Запуск локального веб-сервиса с автоматической перезагрузкой при изменении
  исходного кода и возможностью отладки в IDE
```shell
make dev
```

- Запуск веб-сервиса в продакшене
```shell
make render-start
```

- Завершение работы сервиса: `Ctrl+C`
