# -*- coding: utf-8 -*-
"""
Created on Wed Mar 28 15:22:37 2018

@author: Administrator
"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import re
import time
import pandas as pd


def get_av_list(up_num):
    chrome_options = Options()
    chrome_options.add_argument("--headless")       # define headless
    driver = webdriver.Chrome(chrome_options=chrome_options)
    
    #up_num='883968'#up主ID
    av_all=[]
    driver.get('http://space.bilibili.com/%s#/video'%(up_num,))
    #counter=0
    while(1):    
        html=driver.page_source
        soup = BeautifulSoup(html, features='lxml')
        all_href = soup.find_all('a')
        #print(all_href)
        av_path=re.compile(r'(?<=av)([0-9]+)$')
        for l in all_href:
            data=l.get('href')
            if data:
                if av_path.findall(data):
                    temp=av_path.findall(data)[0]
                    av_all.append(int(temp))
                    
        elements=driver.find_elements_by_class_name('be-pager-next')#点击下一页
        time.sleep(1)
        try:
            elements[0].click()
            time.sleep(1)
        except:
            if av_all==[]:
                continue
            else:
                break
    #开始检测是否每个视频都存在
    av_all=list(set(av_all))
    av_all.sort(reverse=True)#降序
    return av_all


def get_av_info(mid,name,av_list,dict_whole):
    chrome_options = Options()
    chrome_options.add_argument("--headless")       # define headless
    driver = webdriver.Chrome(chrome_options=chrome_options)
    for av in av_list:
        #==========================单个视频的信息======================#
        driver.get('https://www.bilibili.com/video/av%s'%(str(av),))
        html=driver.page_source
        if '视频去哪了呢' in html or '追番' in html:
            av_list.remove(av)#如果视频不存在，丢掉该av，下一个
            print(str(av)+'removed')
            continue
        else:
            pass
        dict_whole['av'].append(av)#视频av号
        dict_whole['up_id'].append(mid)#upID
        dict_whole['up_name'].append(name)#up昵称
        soup = BeautifulSoup(html, features='lxml')

        title=soup.find('h1').text.strip()
        dict_whole['title'].append(title)#视频标题
        
        play_num=re.findall(r'总播放数([0-9]+)',html)[0]
        dict_whole['play_num'].append(int(play_num))#总播放量
        danmu_num=re.findall(r'总弹幕数([0-9]+)',html)[0]
        dict_whole['danmu_num'].append(int(danmu_num))#总弹幕数
        try:
            top_rank=re.findall(r'最高全站日排行([0-9]+)名',html)[0]
            dict_whole['top_rank'].append(int(top_rank))#排行
        except:
            dict_whole['top_rank'].append(0)
        coin_num=re.findall(r'投硬币枚数([0-9]+)',html)[0]
        dict_whole['coin_num'].append(int(coin_num))#硬币数
        fav_num=re.findall(r'收藏人数([0-9]+)',html)[0]
        dict_whole['favorite_num'].append(int(fav_num))#收藏人数
        dict_whole['time'].append(soup.find('time').text)#视频时间
        #分类
        catalog=''
        crumb=soup.find_all('span',attrs={'class':'crumb'})
        for item in crumb:
            catalog=catalog+item.find('a').contents[0]+' '
        dict_whole['catalog'].append(catalog)
        #评论数
        comment=re.findall('itemprop=\"commentCount\" content=\"([0-9]+)\"',html)[0]
        dict_whole['comment_num'].append(int(comment))
        time_local = time.localtime(time.time())
            #转换成新的时间格式(2016-05-05 20:28:54)
        part_date= time.strftime("%Y-%m-%d %H:%M:%S",time_local)
        dict_whole['part_date'].append(part_date)
        #tag
        tag=''
        for item in soup.find_all('li',attrs={'class':'tag'}):
            tag=tag+item.text+' '
        dict_whole['tags'].append(tag)
        print(str(av)+' info_done')
    return av_list
  
def main():
    try:
        df=pd.read_excel('output_up.xlsx')
        up_id=list(df['mid'])#所要爬的up主ID
        up_name=list(df['name'])
        global dict_whole
        dict_whole={'av':[],'up_id':[],'up_name':[],'play_num':[],
                    'danmu_num':[],'coin_num':[],'favorite_num':[],'time':[],
                    'title':[],'top_rank':[],'tags':[],'catalog':[],'comment_num':[],'part_date':[]}
        for mid,name in zip(up_id,up_name):
            print((mid,name))
            av_list=get_av_list(mid)
            print(len(av_list))
            time.sleep(1)
            av_list_final=get_av_info(mid,name,av_list,dict_whole)
            print(len(av_list_final))
    except Exception as e:
        print(e)#错误
    finally:
        writer=pd.ExcelWriter('up_video_info.xlsx')
        df=pd.DataFrame.from_dict(dict_whole,orient='index')
        df=df.transpose()
        df.to_excel(writer,index=False)
        writer.save()
if __name__=='__main__':
    main()
   