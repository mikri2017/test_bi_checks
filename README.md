# test_bi_checks

* checks_server.py - скрипт запускает http сервер, методы:
  * /add_check - добавляет продажу с переданной суммой, GET параметр sum
  * /get_sale_stat - выводит продажи за переданный период, GET параметры date_begin, date_end - начало периода и конец, соответственно. Формат даты: ГГГГ-ММ-ДД
* fill_base_random.py - скрипт наполняет таблицу продаж на июль, август рандомными продажами до 1000
* db_structure/bi_checks.sql - БД проекта под СУБД MariaDB
* db_structure/bi_checks_test_user.sql - пользователь test с правами на доступ к БД проекта
