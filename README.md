# test_bi_checks

* checks_server.py - скрипт запускает http сервер (http://127.0.0.1:8080/), методы:
  * /add_check - добавляет продажу с переданной суммой, GET параметр sum
  * /get_sale_stat - выводит продажи за переданный период, GET параметры date_begin, date_end - начало периода и конец, соответственно. Формат даты: ГГГГ-ММ-ДД
* fill_base_random.py - скрипт наполняет таблицу продаж на июль, август рандомными продажами до 1000
* db_structure/bi_checks.sql - БД проекта под СУБД MariaDB
* db_structure/bi_checks_test_user.sql - пользователь test с правами на доступ к БД проекта
* tg_bot_bi_checks/checks_tg_bot.py - Telegram бот, позволяющий вносить продажи и выводить их за период через http сервис checks_server.py

## Примеры: 
* http://127.0.0.1:8080/add_check?sum=345,87
* http://127.0.0.1:8080/get_sale_stat?date_begin=2021-07-01&date_end=2021-07-31
