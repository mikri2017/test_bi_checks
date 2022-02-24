from tg_bot_mgr import TgBotMgr

tgBot = TgBotMgr()

tgBot.set_api_url("https://api.telegram.org/bot")
tgBot.set_api_token("some_token")
'''
print(tgBot.get_params())

res = tgBot.get_updates()
print(res)
print(type(res))

print("")
'''

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

res = tgBot.send_msg(0, "Выберите дейсвие", buttons)
print(res)
