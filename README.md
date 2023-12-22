# Сервис подбора вакансий

Запуск:

1) Активировать среду и установить все через `pip install -r requirements.txt`
2) Проверить что в .env указаны все нужные переменные среды и в папке `./models/` лежат nmslib веса. [Ссылка на архив.](https://drive.google.com/file/d/11Gl4wk_DRfZhxdIkueWPIvnZBkt9-00Z/view?usp=sharing)
3) Запустить gunicorn сервер `gunicorn main:app -c gunicorn.config.py`
4) Запустить tg бота [@vacnc_bot](https://t.me/vacnc_bot)

___АВГУСТИН ДОПОЛНИ ТУТ___


Информация о ресерче и о производительности лежит [тут.](https://github.com/alex-utk/Vacancy-Recommendation-Service/blob/main/research/results.md)