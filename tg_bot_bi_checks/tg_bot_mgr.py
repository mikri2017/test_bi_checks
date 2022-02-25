import json
import requests
import urllib3

class TgBotMgr():
    def __init__(self):
        self.__tg_api_url = ""
        self.__token = ""
        self.__error_mgr = ""
        # Отключаем предупреждения об SSL
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


    def get_last_error(self):
        return self.__error_mgr


    def set_api_url(self, api_url):
        if api_url != "":
            self.__tg_api_url = api_url
        else:
            self.__error_mgr = "URL API Telegram бота не может быть пустым!"
            return False

        return True


    def set_api_token(self, token):
        if token != "":
            self.__token = token
        else:
            self.__error_mgr = "Token API Telegram не может быть пустым!"
            return False

        return True


    def get_params(self):
        return {
            'url': self.__tg_api_url,
            'token': self.__token
        }


    def get_updates(self, offset = 0):
        url = "%s%s/getUpdates" % (self.__tg_api_url, self.__token)
        if offset > 0:
            url += "?offset=%i" % (offset)

        try:
            res = requests.get(url, verify=False)
            res = res.json()
            if res['ok'] == True:
                return res['result']
            else:
                self.__error_mgr = "Ошибка от Telegram API при получении" \
                    + "обновлений: [%i] %s" % (
                        res['error_code'], res['description']
                    )
                return False
        except Exception as ex:
            self.__error_mgr = "Ошибка получения URL [%s]: %s" % (url, str(ex))
            return False


    def send_msg(self, chat_id, msg, buttons = []):
        """Отправка сообщения

            :param chat_id: ID чата для отправки
            :param msg: Текст сообщения
            :param buttons: Массив словарей для добавления к сообщению кнопок,
                            поля 'text' - подпись кнопки,
                            'callback_data' - идентификатор до 64 байт, для
                            опознания запрошенного пользователем действия
            :return: Словарь результатов
        """

        params = "chat_id=%i&text=%s" % (chat_id, msg)

        inl_buttons = {
            'inline_keyboard': [
                buttons
            ]
        }

        params += "&reply_markup=" + json.dumps(inl_buttons)

        url = "%s%s/sendMessage?%s" % (
            self.__tg_api_url,
            self.__token,
            params
        )

        try:
            res = requests.get(url, verify=False)
            res = res.json()
            if res['ok'] == True:
                return res['result']
            else:
                self.__error_mgr = "Ошибка от Telegram API при отправке" \
                    + " сообщения: [%i] %s" % (
                        res['error_code'], res['description']
                    )
                return False
        except Exception as ex:
            self.__error_mgr = "Ошибка получения URL [%s]: %s" % (url, str(ex))
            return False


    def send_document(self, chat_id, file_path):
        url = "%s%s/sendDocument" % (
            self.__tg_api_url,
            self.__token
        )

        params = {'chat_id': chat_id}

        try:
            with open(file_path, "rb") as f:
                res = requests.post(url, data=params, files={'document': f}, verify=False)
                res = res.json()
                if res['ok'] == True:
                    return res['result']
                else:
                    self.__error_mgr = "Ошибка от Telegram API при отправке" \
                        + " файла %s: [%i] %s" % (
                            file_path, res['error_code'], res['description']
                        )
                    return False
        except Exception as ex:
            self.__error_mgr = "Ошибка получения URL [%s]: %s" % (url, str(ex))
            return False
