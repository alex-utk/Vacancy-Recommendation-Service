# Сервис подбора вакансий

Запуск:

1) Активировать среду и установить все через `pip install -r requirements.txt`
2) Проверить что в .env указаны все нужные переменные среды и в папке `./models/` лежат nmslib веса. [Ссылка на архив.](https://drive.google.com/file/d/11Gl4wk_DRfZhxdIkueWPIvnZBkt9-00Z/view?usp=sharing)
3) Запустить gunicorn сервер `gunicorn main:app -c gunicorn.config.py`
4) Запустить tg бота [@vacnc_bot](https://t.me/vacnc_bot)
5) ввести команду /start
6) После этого нажать на одну из кнопок Job Seeker для соискателей или HR для ищущих вакансии
7) После выбора Job Seeker нужно будет ответить на вопросы и получить рекомендации по вакансиям
8) После выбора HR нужно будет ответить на вопросы бота и получить уже рекомендации по подходящим резюме


Информация о ресерче и о производительности лежит [тут.](https://github.com/alex-utk/Vacancy-Recommendation-Service/blob/main/research/results.md)