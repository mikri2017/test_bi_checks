def check_tg_upd_data(upd_inf):
    res = {
        'type': "",
        'data': {}
    }

    if 'callback_query' in upd_inf.keys():
        # Произошло нажатие кнопки
        res['type'] = "btn_pressed"
        res['data']['upd_id'] = upd_inf['update_id']
        res['data']['chat_id'] = upd_inf['callback_query']['from']['id']
        res['data']['btn_type'] = upd_inf['callback_query']['data']
    elif 'message' in upd_inf.keys():
        # Пришло сообщение
        res['type'] = "msg"
        res['data']['upd_id'] = upd_inf['update_id']
        res['data']['chat_id'] = upd_inf['message']['from']['id']
        res['data']['msg'] = upd_inf['message']['text']

    return res


def send_bot_hello_msg(tg_bot, chat_id):
    msg = "Выберите дейсвие"

    buttons = [
        {
            'text': "Внести продажу",
            'callback_data': "add_check"
        },
        {
            'text': "Продажи за период",
            'callback_data': "get_report"
        }
    ]

    return tg_bot.send_msg(chat_id, msg, buttons)