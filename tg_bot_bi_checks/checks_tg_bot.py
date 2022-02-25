from decimal import Decimal
from time import sleep
from datetime import datetime
from tg_bot_mgr import TgBotMgr
import checks_tg_bot_common as chc

tg_bot = TgBotMgr()

tg_bot.set_api_url("https://api.telegram.org/bot")
tg_bot.set_api_token("some_token")

info_msg = "Получаем ID последнего обновления дальнейшей работы"
print(info_msg)

last_upd_id = 0
res = tg_bot.get_updates()
if res['ok'] == True:
    for upd in res['result']:
        if upd['update_id'] > last_upd_id:
            last_upd_id = upd['update_id']

info_msg = "ID последнего обновления: %i" % (last_upd_id)
print(info_msg)

# Хост сайта http сервиса статистики продаж
bi_checks_host = "127.0.0.1:8080"

# Состояния пользователей
users_stat = {}

while 1:
    # Проверяем на наличие новых запросов
    res = tg_bot.get_updates()
    if res['ok'] == True:
        for upd in res['result']:
            if upd['update_id'] > last_upd_id:
                # Обработка обновления
                res = chc.check_tg_upd_data(upd)
                if res['type'] == "msg":
                    if res['data']['msg'] == "/start":
                        res_msg = chc.send_bot_hello_msg(
                            tg_bot,
                            res['data']['chat_id']
                        )
                    elif res['data']['chat_id'] in users_stat.keys():
                        status = users_stat[res['data']['chat_id']]
                        if status == 0:
                            # Пришла сумма продажи
                            msg = res['data']['msg'].replace(',', '.').strip()
                            try:
                                check_sum = Decimal(msg)
                                add_check_res = chc.add_check(bi_checks_host, check_sum)
                                if add_check_res['res'] == "ok":
                                    send_msg = "Продажа на сумму %s внесена успешно" % (add_check_res['sum'])
                                else:
                                    send_msg = add_check_res['msg']
                                tg_bot.send_msg(res['data']['chat_id'], send_msg)
                            except Exception as ex:
                                error_msg = "Передано некорректное значение " \
                                    + "cуммы: %s" % (msg)
                                tg_bot.send_msg(res['data']['chat_id'], error_msg)

                                error_msg += ", текст ошибки: %s" % (str(ex))
                                print(error_msg)
                        elif status == 1:
                            msg_dates = res['data']['msg'].strip().split(" ")
                            date_begin = ""
                            date_end = ""
                            if len(msg_dates) == 2:
                                try:
                                    date_begin = datetime.strptime(msg_dates[0], "%Y-%m-%d")
                                    date_end = datetime.strptime(msg_dates[1], "%Y-%m-%d")

                                    stat_res = chc.get_check_stat(bi_checks_host, date_begin, date_end)
                                    if stat_res == "err":
                                        tg_bot.send_msg(res['data']['chat_id'], stat_res['msg'])
                                    else:
                                        # Собираем сообщение с полученной статистикой
                                        send_msg = ""
                                        if len(stat_res['items']) == 0:
                                            send_msg = "Данных за выбранный период нет"
                                        else:
                                            send_msg = chc.gen_check_stat_res_msg(stat_res['items'])
                                            if send_msg == "":
                                                send_msg = "Данные отсутствуют"
                                        tg_bot.send_msg(res['data']['chat_id'], send_msg)
                                except ValueError:
                                    error_msg = "Даты не соответствуют формату: %s" % (
                                        res['data']['msg']
                                    )
                                    tg_bot.send_msg(res['data']['chat_id'], error_msg)
                            else:
                                error_msg = "Даты не соответствуют формату: %s" % (
                                    res['data']['msg']
                                )
                                tg_bot.send_msg(res['data']['chat_id'], error_msg)
                        else:
                            error_msg = "Пользователь %i имеет неизвестный статус %i" % (
                                res['data']['chat_id'],
                                status
                            )
                            print(error_msg)

                            error_msg = "Внутренняя ошибка, повторите запрос"
                            tg_bot.send_msg(res['data']['chat_id'], error_msg)

                        del(users_stat[res['data']['chat_id']])
                    else:
                        info_msg = "Сообщение не опознано, для выбора действия, " \
                            + "нажмите кнопку"
                        tg_bot.send_msg(res['data']['chat_id'], info_msg)

                    res_msg = chc.send_bot_hello_msg(
                        tg_bot,
                        res['data']['chat_id']
                    )
                elif res['type'] == "btn_pressed":
                    if res['data']['btn_type'] == "add_check":
                        info_msg = "Отправьте следующим сообщением сумму"
                        tg_bot.send_msg(res['data']['chat_id'], info_msg)

                        # Устанавливаем статус приема суммы продажи
                        users_stat[res['data']['chat_id']] = 0
                    elif res['data']['btn_type'] == "get_report":
                        info_msg = "Отправьте следующим сообщением период в " \
                            + "формате:\r\nГГГГ-ММ-ДД ГГГГ-ММ-ДД"
                        tg_bot.send_msg(res['data']['chat_id'], info_msg)

                        # Устанавливаем статус приема начальной даты
                        users_stat[res['data']['chat_id']] = 1
                    else:
                        info_msg = "Получен неизвестный запрос"
                        tg_bot.send_msg(res['data']['chat_id'], info_msg)

                        if res['data']['chat_id'] in users_stat.keys():
                            del(users_stat[res['data']['chat_id']])

                        res_msg = chc.send_bot_hello_msg(
                            tg_bot,
                            res['data']['chat_id']
                        )

                last_upd_id = upd['update_id']
    sleep(3)
