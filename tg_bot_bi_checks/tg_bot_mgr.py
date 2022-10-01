import os
import json
import requests
from io import BytesIO
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
        :return: Словарь результатов или False при ошибке
        """

        url = "%s%s/sendMessage" % (
            self.__tg_api_url,
            self.__token
        )

        params = {
            'chat_id': chat_id,
            'parse_mode': "HTML",
            'text': msg
        }

        inl_buttons = {
            'inline_keyboard': [
                buttons
            ]
        }

        params['reply_markup'] = json.dumps(inl_buttons)

        try:
            res = requests.get(url, params=params, verify=False)
            res = res.json()
            if res['ok'] == True:
                return [res['result']]
            else:
                self.__error_mgr = "Ошибка от Telegram API при отправке" \
                    + " сообщения: [%i] %s" % (
                        res['error_code'], res['description']
                    )
                return False
        except Exception as ex:
            self.__error_mgr = "Ошибка получения URL [%s]: %s" % (url, str(ex))
            return False


    def send_document(self, chat_id, file_path, caption = ""):
        url = "%s%s/sendDocument" % (
            self.__tg_api_url,
            self.__token
        )

        params = {
            'chat_id': chat_id,
            'parse_mode': "HTML",
            'caption': caption
        }

        try:
            with open(file_path, "rb") as f:
                res = requests.post(url, data=params, files={'document': f}, verify=False)
                res = res.json()
                if res['ok'] == True:
                    return [res['result']]
                else:
                    self.__error_mgr = "Ошибка от Telegram API при отправке" \
                        + " файла %s: [%i] %s" % (
                            file_path, res['error_code'], res['description']
                        )
                    return False
        except Exception as ex:
            self.__error_mgr = "Ошибка получения URL [%s]: %s" % (url, str(ex))
            return False


    def send_document_by_file_id(self, chat_id, file_id, caption = ""):
        url = "%s%s/sendDocument" % (
            self.__tg_api_url,
            self.__token
        )

        params = {
            'chat_id': chat_id,
            'parse_mode': "HTML",
            'document': file_id,
            'caption': caption
        }

        try:
            res = requests.get(url, params=params, verify=False)
            res = res.json()
            if res['ok'] == True:
                return [res['result']]
            else:
                self.__error_mgr = "Ошибка от Telegram API при отправке" \
                    + " сообщения: [%i] %s" % (
                        res['error_code'], res['description']
                    )
                return False
        except Exception as ex:
            self.__error_mgr = "Ошибка получения URL [%s]: %s" % (url, str(ex))
            return False


    def send_photo(self, chat_id, file_path, caption = ""):
        url = "%s%s/sendPhoto" % (
            self.__tg_api_url,
            self.__token
        )

        params = {
            'chat_id': chat_id,
            'parse_mode': "HTML",
            'caption': caption
        }

        try:
            with open(file_path, "rb") as f:
                res = requests.post(url, data=params, files={'photo': f}, verify=False)
                res = res.json()
                if res['ok'] == True:
                    return [res['result']]
                else:
                    self.__error_mgr = "Ошибка от Telegram API при отправке" \
                        + " файла %s: [%i] %s" % (
                            file_path, res['error_code'], res['description']
                        )
                    return False
        except Exception as ex:
            self.__error_mgr = "Ошибка получения URL [%s]: %s" % (url, str(ex))
            return False


    def send_photo_by_file_id(self, chat_id, file_id, caption = ""):
        """Отправка фото по file_id от Telegram
        """

        url = "%s%s/sendPhoto" % (
            self.__tg_api_url,
            self.__token
        )

        params = {
            'chat_id': chat_id,
            'parse_mode': "HTML",
            'photo': file_id,
            'caption': caption
        }

        try:
            res = requests.get(url, params=params, verify=False)
            res = res.json()
            if res['ok'] == True:
                return [res['result']]
            else:
                self.__error_mgr = "Ошибка от Telegram API при отправке" \
                    + " сообщения: [%i] %s" % (
                        res['error_code'], res['description']
                    )
                return False
        except Exception as ex:
            self.__error_mgr = "Ошибка получения URL [%s]: %s" % (url, str(ex))
            return False


    def send_media_group_photos(self, chat_id, paths_with_captions):
        """Отправка группы фотографий в виде альбома
        :param chat_id: ID чата для отправки
        :param paths_with_captions: Словарь "Подпись": "Путь к файлу"
        :return: Словарь результатов или False при ошибке
        """

        url = "%s%s/sendMediaGroup" % (
            self.__tg_api_url,
            self.__token
        )
    
        files = {}
        media = []

        msg = ""
        first = True
        try:
            for caption, path in paths_with_captions.items():
                f_img = open(path, "rb")
                with BytesIO(f_img.read()) as b_out:
                    b_out.seek(0)
                    name = os.path.basename(path)
                    files[name] = b_out.read()
                    media.append(
                        dict(
                            type='photo',
                            media=f'attach://{name}',
                            parse_mode="HTML",
                            caption=caption
                        )
                    )

                if first:
                    msg += caption
                    first = False
                else:
                    msg += "\n%s" % (caption)

                f_img.close()
        except Exception as ex:
            self.__error_mgr = "Ошибка получения URL [%s]: %s" % (url, str(ex))
            return False

        params = {
            'chat_id': chat_id,
            'media': json.dumps(media),
            'parse_mode': "HTML",
            'caption': msg
        }

        try:
            res = requests.post(url, data=params, files=files, verify=False)
            res = res.json()
            if res['ok'] == True:
                return res['result']
            else:
                self.__error_mgr = "Ошибка от Telegram API при отправке" \
                    + " группы фото: [%i] %s" % (
                        res['error_code'], res['description']
                    )
                return False
        except Exception as ex:
            self.__error_mgr = "Ошибка получения URL [%s]: %s" % (url, str(ex))
            return False


    def send_media_group_photos_by_file_id(self, chat_id, file_ids_with_captions):
        """Отправка группы фотографий в виде альбома
        :param chat_id: ID чата для отправки
        :param file_ids_with_captions: Словарь "Подпись": file_id
        :return: Словарь результатов или False при ошибке
        """

        url = "%s%s/sendMediaGroup" % (
            self.__tg_api_url,
            self.__token
        )
    
        files = {}
        media = []

        msg = ""
        first = True
        for caption, file_id in file_ids_with_captions.items():
            media.append(
                dict(
                    type='photo',
                    media=file_id,
                    parse_mode="HTML",
                    caption=caption
                )
            )

            if first:
                msg += caption
                first = False
            else:
                msg += "\n%s" % (caption)

        params = {
            'chat_id': chat_id,
            'media': json.dumps(media),
            'parse_mode': "HTML",
            'caption': msg
        }

        try:
            res = requests.get(url, data=params, verify=False)
            res = res.json()
            if res['ok'] == True:
                return res['result']
            else:
                self.__error_mgr = "Ошибка от Telegram API при отправке" \
                    + " группы фото по их file_id: [%i] %s" % (
                        res['error_code'], res['description']
                    )
                return False
        except Exception as ex:
            self.__error_mgr = "Ошибка получения URL [%s]: %s" % (url, str(ex))
            return False
