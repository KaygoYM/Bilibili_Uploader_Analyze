# -*- coding: utf-8 -*-
"""
Created on Wed Mar 28 15:22:37 2018

@author: Administrator
"""
import re
import requests
#from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import time
import multiprocessing as mp


def getVideos():
    pass

def getdanmu(av):
    #global danmu_dict
    #danmu_dict={'color':[],'content':[],'create_time':[],
     #           'pattern':[],'size':[],'pool':[],'row_ID':[],'sender_ID':[],
      #          'time_stamp':[],'av':[],'part_date':[]}
    #danmu_dict={}
    danmu_file=open('danmu_all.txt','a+',encoding='utf-8')
    try:
        url = "http://www.bilibili.com/video/av"+str(av)+"/"
        headers={'User-Agent':"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)",}
        u = requests.get(url=url,headers=headers)
        html = u.text
        cid = re.findall(r'cid=(.*?)&',html)[0]
        dmurl = "http://comment.bilibili.com/"+str(cid)+".xml"
        dmhtml = requests.get(dmurl).text
        #soup = BeautifulSoup(dmhtml, 'lxml')
        #danmu=soup.find_all('d')
        #print(danmu)
            #soup = bs(dmhtml,'xml')
        danmu_path=re.compile('<d p="(.+?),(.+?),(.+?),(.+?),(.+?),(.+?),(.+?),(.+?)">(.+?)</d>')
        dmlist = danmu_path.findall(dmhtml)
        #danmu_array=np.array(dmlist)
        #danmu_dict={}
            #为存入Excel准备
        for j in dmlist:
            time_local = time.localtime(time.time())
            #转换成新的时间格式(2016-05-05 20:28:54)
            part_date= time.strftime("%Y-%m-%d %H:%M:%S",time_local)
            lines=[str(sec_to_str(j[0]))+'\t'+str(j[1])+'\t'+
                   str(j[2])+'\t'+str(j[3])+'\t'+str(time.ctime(eval(j[4])))+'\t'+
                   str(j[5])+'\t'+str(j[6])+'\t'+str(j[7])+'\t'+
                   str(j[8])+'\t'+str(av)+'\t'+str(part_date)]
            danmu_file.writelines(lines)
            danmu_file.write('\n')
        print(str(av)+' danmu_done')
    except Exception as e:
        print(e)
        print(av)
        #getHTMLText(writer,url,av)
    finally:
        pass
    
    
def sec_to_str(seconds):
    seconds = eval(seconds)
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    dtEventTime = "%02d:%02d:%02d" % (h, m, s)
    return (dtEventTime)

'''
<d p="533.67199707031,1,25,41194,1498943949,0,7edeebe9,3511616609">刀还是没有枪快</d>
2.5     p这个字段里面的内容：（资料来自百度搜索）
0,1,25,16777215,1312863760,0,eff85771,42759017中几个逗号分割的数据
第0个参数是弹幕出现的时间以秒数为单位。
第1个参数是弹幕的模式1..3 滚动弹幕 4底端弹幕 5顶端弹幕 6.逆向弹幕 7精准定位 8高级弹幕
第2个参数是字号， 12非常小,16特小,18小,25中,36大,45很大,64特别大
第3个参数是字体的颜色以HTML颜色的十进制为准
第4个参数是Unix格式的时间戳。基准时间为 1970-1-1 08:00:00
第5个参数是弹幕池 0普通池 1字幕池 2特殊池【目前特殊池为高级弹幕专用】
第6个参数是发送者的ID，用于“屏蔽此弹幕的发送者”功能
第7个参数是弹幕在弹幕数据库中rowID 用于“历史弹幕”功能。
''' 
def main():
    try:
        df=pd.read_excel('up_video_info.xlsx')
        av_list=list(df['av'])
        av_list.sort()#up_name_list=list(df['up_name'])
        #up_id_list=list(df['up_id'])
        print(av_list)
        
        #for av in av_list:
        pool=mp.Pool(processes=10)
        pool.map(getdanmu,(av_list))
            #getdanmu(av)
        #print(res)
        #file = open('res.pickle', 'wb')
        #pickle.dump(res, file)
        #file.close()
           #print(str(av)+'danmu done')
        pool.join()
    except Exception as e:
        print(e)
    finally:
        pass
        #df=pd.DataFrame.from_dict(res,orient='index')
        #df=df.transpose()
        #df.to_csv('danmu_all.txt',sep='\t',index=False)


if __name__ == "__main__":
    main()
    