import requests

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


def add_check(bi_checks_host, sum):
    res = {
        'res': "ok"
    }

    url = "http://%s/add_check?sum=%s" % (bi_checks_host, str(sum))

    try:
        req_res = requests.get(url)
        answer = req_res.json()
        if answer['res'] == "ok":
            res['sum'] = answer['sum']
        else:
            res['res'] = "err"
            res['msg'] = answer['msg']
            return res
    except Exception as ex:
        res['res'] = "err"
        res['msg'] = "Ошибка получения URL [%s]: %s" % (url, str(ex))

    return res


def get_check_stat(bi_checks_host, date_begin, date_end):
    res = {
        'res': "ok"
    }

    url = "http://%s/get_sale_stat?date_begin=%s&date_end=%s" % (
        bi_checks_host,
        date_begin.strftime("%Y-%m-%d"),
        date_end.strftime("%Y-%m-%d")
    )

    try:
        req_res = requests.get(url)
        answer = req_res.json()
        if answer['res'] == "ok":
            res['items'] = answer['items']
        else:
            res['res'] = "err"
            res['msg'] = answer['msg']
    except Exception as ex:
        res['res'] = "err"
        res['msg'] = "Ошибка получения URL [%s]: %s" % (url, str(ex))

    return res
