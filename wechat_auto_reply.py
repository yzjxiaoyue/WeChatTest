from wxpy import *

# 以下api_key是在图灵机器人官网注册图灵机器人的api_key
turing = Tuling(api_key='b483cceec48942528ca64021117050**')
bot = Bot()

# 只跟某一个好友聊天，比如你的好友昵称是 “我嘞个去”
someone = bot.friends().search('我嘞个去')


@bot.register(chats=someone)
def community(msg):
    resp = turing.do_reply(msg)


bot.join()
