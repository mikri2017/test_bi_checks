import requests

class TgBotMgr():
    def __init__(self):
        self.__tg_api_url = ""
        self.__token = ""
        self.__error_mgr = ""


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


    def get_updates(self):
        req_url = "%s%s/getUpdates" % (self.__tg_api_url, self.__token)
        res = requests.get(req_url)
        return res.json()


    def send_msg(self, chat_id, msg):
        params = "chat_id=%i&text=%s" % (chat_id, msg)

        req_url = "%s%s/sendMessage?%s" % (
            self.__tg_api_url,
            self.__token,
            params
        )

        res = requests.get(req_url)
        return res.json()
