import itchat
from pyecharts import Pie, Map
import pandas as pd
import re
import jieba
import wordcloud as wc
import numpy as np
import PIL.Image as Image
import matplotlib.pyplot as plt

# 登录并发送信息到文件助手
itchat.auto_login()
itchat.send('Hello, filehelper', toUserName='filehelper')

# 好友性别分析
friends = itchat.get_friends(update=True)[0:]
print(friends)
boy = girl = nothing = 0
for i in friends[1:]:
    sex = i["Sex"]
    if sex == 1:
        boy += 1
    elif sex == 2:
        girl += 1
    else:
        NickName = i["NickName"]
        print(NickName)
        nothing += 1
total = len(friends[1:])
attr = ["迷妹", "迷弟", "低调的匿名粉丝"]
v1 = [boy, girl, nothing]
pie = Pie("粉丝性别分布", title_pos='center')
pie.add("", attr, v1, radius=[40, 75], label_text_color=None, is_label_show=True, is_legend_show=False)
pie.show_config()
pie.render("./sex_data.html")

siglist = []
for i in friends:
    print(i['RemarkName'], '\'' + i['NickName'] + '\'', i['Signature'])
    signature = i['Signature'].strip().replace("span", "").replace("class", "").replace("emoji", "")
    rep = re.compile("1f\d+\w*|[<>/=]")
    signature = rep.sub("", signature)
    siglist.append(signature)
    text = "".join(siglist)
wordlist = jieba.cut(text, cut_all=True)
word_space_split = " ".join(wordlist)
coloring = np.array(Image.open("./1.jpg"))  # 一张猴子图片,试了很多照片，还是这个好
my_wordcloud = wc.WordCloud(background_color="white",  # 背景颜色
                            mask=coloring, max_words=1000,  # 最大词数
                            max_font_size=60,  # 字体最大值
                            random_state=42, scale=4,  # 按照比例进行放大画布，如设置为1.5，则长和宽都是原来画布的1.5倍。
                            font_path="./HYQiHei50S.ttf",  # 字体，注意选择合适的字体，否则可能会显示乱码。
                            width=400, height=200  # 像素
                            ).generate(word_space_split)
image_colors = wc.ImageColorGenerator(coloring)  # plt.imshow(my_wordcloud.recolor(color_func=image_colors))
plt.imshow(my_wordcloud)
plt.axis("off")  # 不显示坐标轴
plt.show()
my_wordcloud.to_file('./test.jpg')


#  地理分布
def get_var(var):
    variable = []
    for i in friends:
        value = i[var]
        variable.append(value)
    return variable


NickName = get_var("NickName")
Sex = get_var("Sex")
Province = get_var('Province')
Signature = get_var('Signature')
city = get_var('City')
data = {'NickName': NickName, 'Sex': Sex, 'Province': Province, 'Signature': Signature, 'city': city}
frame = pd.DataFrame(data)
result1 = frame.groupby(['Province'], as_index=False).size()
a1 = list(result1)
a2 = result1.index
map = Map("我的好友占了大半个中国啊！", "来自微信的朋友圈", title_pos="center", width=1200, height=600)
map.add("", a2, a1, maptype='china', is_visualmap=True, visual_text_color='#000', visual_range=[1, 8],
        is_label_show=True, symbol="diamon", label_pos="inside")
map.show_config()
map.render("./area_data.html")
