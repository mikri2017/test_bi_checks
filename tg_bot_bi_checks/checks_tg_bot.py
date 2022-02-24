from tg_bot_mgr import TgBotMgr

tgBot = TgBotMgr()

tgBot.set_api_url("https://api.telegram.org/bot")
tgBot.set_api_token("some_token")

print(tgBot.get_params())

res = tgBot.get_updates()
print(res)
print(type(res))

print("")
res = tgBot.send_msg(0, "Test some")
print(res)
