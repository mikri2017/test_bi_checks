from time import sleep
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
                        print(res_msg)
                elif res['type'] == "btn_pressed":
                    if res['data']['btn_type'] == "add_check":
                        info_msg = "Получен запрос на добавление продажи"
                        tg_bot.send_msg(res['data']['chat_id'], info_msg)
                    elif res['data']['btn_type'] == "get_report":
                        info_msg = "Получен запрос на получение отчета"
                        tg_bot.send_msg(res['data']['chat_id'], info_msg)
                    else:
                        info_msg = "Получен неизвестный запрос"
                        tg_bot.send_msg(res['data']['chat_id'], info_msg)

                    res_msg = chc.send_bot_hello_msg(tg_bot, res['data']['chat_id'])

                last_upd_id = upd['update_id']
    sleep(3)
