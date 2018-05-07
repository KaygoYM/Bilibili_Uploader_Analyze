Bilibili UP_information Scrapy
====
DEMO version || Fin version
----
本项目抽取数据为 **HIVE**</br>
本项目所使用的数据可视化为 **Excel**</br>
Using **HIVE** to analyze this project's data.</br>
Using **Excel** to visualize this project's result.</br>

**该爬虫仅供学习使用!**</br>
**This project is for learning only!** </br>

## 文件介绍_Introduction

* `user_bilibili.py`：爬取up主信息的文件</br>
For uploaders' personal information</br>
* `video_info_for_up_bilibili.py`：爬取up主所有视频信息的文件</br>
For all the information of the uploaders' videos</br>
* `danmu_bilibili.py`：弹幕下载器(注意只能爬当前弹幕池的弹幕，非所有历史弹幕)</br>
For the barrage of all the videos(Tips:Only for the barrage in current POOL)</br>
* `danmu_wordcloud.py`：所给弹幕的词云</br>
For the wordcloud of the given barrage</br>
* `av_to_comment.py`：生成"哔哩哔哩AV号.txt"以便使用评论抓取.exe抓取评论</br>
Generating "哔哩哔哩AV号.txt" which will be further used by the exe</br>
* `哔哩哔哩视频评论抓取by墨问非名[beta][20180322].exe`：抓取评论</br>
Scraping all the comments in the videos</br>
* `comment_bilibili.py`：处理评论信息</br>
Dealing with the comments' information</br>
* `Hive_HQL.sql`：一些抽取数据的HQL/SQL脚本</br>
The HQL/SQL script for extracting data</br>

## Bilibili_UP主成绩报告(DEMO)
* 以屎蛋(STN工作室)和狮子(吃素的狮子)为例：[stn_vs_lion_s2.xlsx](https://github.com/KaygoYM/Bilibili_Uploader_Analyze/blob/master/stn_vs_lion_s2.xlsx)</br>
* 各区Up主代表成绩数据：[uploaders.xlsx](https://github.com/KaygoYM/Bilibili_Uploader_Analyze/blob/master/uploaders.xlsx)</br>

**跪求Star Orz...**</br>

## UP主成绩初步分析(DEMO)
### 基本概况

- 总UP数：19(选取各区个人比较喜欢的UP主，使用时各位可随意发挥)</br>
hanser、泠鸢yousa||papi酱||凉风有性胖次君、LexBurner||赤九玖、咬人猫||暴走漫画、木鱼水心、谷阿莫||</br>
渗透之C君、STN工作室、怕上火暴王老菊、敖厂长、神奇陆夫人、逍遥散人、黑桐谷歌||吃素的狮子、茶几君梦二||</br>

- 抓取用户所有视频存入数据库但抽取近一年的视频作品作为样本分析：(发稿日期)2017.04.01—2018.04.18</br>
- 抓取字段：共四张表，具体字段详见程序。</br>

### 产量
![产量](https://github.com/KaygoYM/Bilibili_Uploader_Analyze/blob/master/Pictures/video_num.png)</br>
可以看到这一年当中，`影视区`的up主普遍高产，`游戏区`次之。其中陆夫人554个视频堪称“母猪”。</br>

### 播放量
![播放量](https://github.com/KaygoYM/Bilibili_Uploader_Analyze/blob/master/Pictures/avg_playnum.png)</br>
**咬人猫、敖厂长、papi酱**的均播放量为前三甲。</br>
影视区和游戏区其他up主则因为视频数基数大，这一指标有所影响。</br>

### 硬币数
![硬币数](https://github.com/KaygoYM/Bilibili_Uploader_Analyze/blob/master/Pictures/avg_coinnum.png)</br>
**敖厂长**的均硬币数遥遥领先，有5w+之多，可见其《囧的呼唤》系列视频之精。“哥们”可谓非常良心了。</br>

### 弹幕量
![弹幕量](https://github.com/KaygoYM/Bilibili_Uploader_Analyze/blob/master/Pictures/avg_danmunum.png)</br>
**C菌**的均弹幕量和**敖厂长**旗鼓相当，并达到4w+;第二集团则有**散人**和**蕾丝**，达到2w左右。</br>
他们的视频内容更吸引大家发送弹幕吐槽。</br>

### 收藏量
![收藏量](https://github.com/KaygoYM/Bilibili_Uploader_Analyze/blob/master/Pictures/avg_favnum.png)</br>
**咬人猫**的均收藏量达到惊人的3w+，结合其播放量，可见咬人猫非常受欢迎，其视频会被反复观看。</br>
`鬼畜区`、`音乐区`和`动画区`收藏量都不错，游戏区和影视区则偏少。可能和视频内容以及定位有关。</br>

### 评论数
![评论数](https://github.com/KaygoYM/Bilibili_Uploader_Analyze/blob/master/Pictures/avg_comnum.png)</br>
B站评论区是观众留言讨论的地方。**蕾丝**的动画吐槽、影评、广告等视频更吸引大家留下自己的见解，每个视频平均有7000+条评论。(包含楼中楼)</br>

**非常适合做广告啊啊啊啊啊！**</br>

### 评论观众质量评估(以屎蛋和狮子为例，其他up主依次可做)</br>
抽取所有在屎蛋和狮子近一年的视频中发表评论的用户数据。</br>
![观众等级](https://github.com/KaygoYM/Bilibili_Uploader_Analyze/blob/master/Pictures/audience_level.png)</br>
可见，大多观看他们视频并留言的观众大多为 **4、5级**</br>
屎蛋和狮子观众的平均等级分别为 **4.45** 和 **4.20**</br>
两位up主的粉丝交集占两者总观众**7%**，因而从留言评论的角度来看，两位up主粉丝交集一般。</br>

![观众VIP](https://github.com/KaygoYM/Bilibili_Uploader_Analyze/blob/master/Pictures/audience_vip.png)</br>
会员方面，两者的留言观众中，非会员部分均超过了50%。具体会员/非会员比：屎蛋为**0.96:1**；狮子为**0.72:1**</br>

### 词云(以屎蛋和狮子为例，其他up主依次可做)
屎蛋的抽样弹幕词云：</br>
![屎蛋词云](https://github.com/KaygoYM/Bilibili_Uploader_Analyze/blob/master/Pictures/stn_danmu.png)</br>
狮子的抽样弹幕词云：</br>
![狮子词云](https://github.com/KaygoYM/Bilibili_Uploader_Analyze/blob/master/Pictures/lion_danmu.png)</br>
大家自行体会吧。(ง•̀_•́)ง </br>

## 鸣谢 Thanks
[airingursb](https://github.com/airingursb/bilibili-user)
