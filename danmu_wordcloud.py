# -*- coding: utf-8 -*-
"""
Created on Tue Apr 17 18:02:29 2018

@author: Administrator
"""

import pandas as pd
import jieba
import jieba.posseg as psg
from collections import Counter
import matplotlib.pyplot as plt
from wordcloud import WordCloud,STOPWORDS,ImageColorGenerator
danmu=list(pd.read_excel('stn_danmu.xlsx')['content'])
danmu=[str(i) for i in danmu]
danmu_all=''.join(danmu)
jieba.add_word('黄旭东')
jieba.add_word('屎蛋')
danmu_words_flags=[(x.word,x.flag) for x in psg.cut(danmu_all)]#获取词的属性以便过滤
stop_attr = ['a','b','c','d','f','df','p','r','rr','s','t','u','ule','ude1','v','z','x','y','e','m','mq']
stop_word = ['了','的','吧','吗','个','人','部','1','2','3','4','一','哈哈哈哈','哈哈']
danmu_words = [x[0] for x in danmu_words_flags if x[1] not in stop_attr and x[0] not in stop_word]
count_danmu_words=dict(Counter(danmu_words).most_common(100))
backgroud_Image = plt.imread('stn.jpg')
#backgroud_Image = plt.imread('cover_love.jpg')
wc = WordCloud( background_color = 'white',    # 设置背景颜色
                mask = backgroud_Image,        # 设置背景图片
                max_words = 200,            # 设置最大现实的字数
                stopwords = STOPWORDS,        # 设置停用词
                font_path = './fonts/simhei.ttf',# 设置字体格式，如不设置显示不了中文
                max_font_size = 100,# 设置字体最大值
                #width=1000,
                #height=860,
                #min_font_size = 10,               
                random_state = 24,            # 设置有多少种随机生成状态，即有多少种配色方案
                )
wc.generate_from_frequencies(count_danmu_words)
image_colors = ImageColorGenerator(backgroud_Image)
wc.recolor(color_func = image_colors)
plt.imshow(wc)
plt.axis('off')
plt.savefig('stn_danmu.png',dpi=600)