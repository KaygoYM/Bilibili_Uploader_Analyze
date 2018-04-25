# -*- coding: utf-8 -*-
"""
Created on Tue Apr 10 17:22:52 2018

@author: Administrator
"""

from os import listdir
import time
import user_bilibili
import requests
import json
import multiprocessing as mp

def add_sub_comment(all_comments_dict,current_up_id):
    for each in all_comments_dict:#对每一楼
        av=str(int(each['oid']))
        c_up_id=str(current_up_id)
        c_content=each['content']['message'].replace('\t','').replace('\n','')
        user_id=str(int(each['mid']))
        user_sex=str(each['member']['sex'])
        user_name=each['member']['uname']
        user_level=str(int(each['member']['level_info']['current_level']))
        user_vip=str(int(each['member']['vip']['vipStatus']))
        time_local = time.localtime(time.time())
        #转换成新的时间格式(2016-05-05 20:28:54)
        part_date= time.strftime("%Y-%m-%d %H:%M:%S",time_local)
        part_date=str(part_date)
        #开始处理该用户的其他信息
        '''
        jsdata=user_bilibili.request_data(user_bilibili.UserAgent(),user_id)
        if jsdata['status']==True:
            data=jsdata['data']
        #print(data)
            user_sex=str(data['sex'] if data['sex']!='' else 'None')#用户性别
            user_coins=str(data['coins'])#用户B币数
            try:
                user_birthday=str(data['birthday'])#生日
            except:
                user_birthday='None'
            try:
                user_place=str(data['place'] if data['place']!=''  else 'None')#注册地
            except:
                user_place='None'
            try:
                regtime=time.localtime(data['regtime'])
                regtime=time.strftime('%Y-%m-%d',regtime)
                user_regtime=str(regtime)#用户注册时间
            except:
                user_regtime=str('None')
            #print(item)
        #follower_num and following_num
            
        try:
            res = requests.get('https://api.bilibili.com/x/relation/stat?vmid='+str(user_id)+'&jsonp=jsonp&').text
            js_fans_data = json.loads(res)
            following = js_fans_data['data']['following']
            fans = js_fans_data['data']['follower']
            user_following_num=str(following)
            user_fans_num=str(fans)
        except Exception as e:
            print(e)
            time.sleep(10)
        '''
        comment_file=open('comment_all.txt','a+',encoding='utf-8')
        lines=[av+'\t'+c_up_id+'\t'+c_content+'\t'+
               user_id+'\t'+user_name+'\t'+user_level+'\t'+
               user_vip+'\t'+user_sex+'\t'+part_date+'\t']
        comment_file.writelines(lines)
        time.sleep(0.1)
        comment_file.write('\n')
            #comment_file.close()
        #如果有楼中楼的回复，迭代调用,处理楼中楼
        if each['replies']!=[] and each['replies'] is not None:
            add_sub_comment(each['replies'],current_up_id)
        else:
            pass
    print(str(av)+"comment_done")
#将文件夹内的文件名读进列表m
def add_comment(file_name):
    filepath='.\Bilibili'
    with open(filepath+"\\"+file_name,'r') as load_f:
        load_dict = json.load(load_f)
        all_comments=load_dict['data']['replies']#replies就是楼层
        current_up_id=int(load_dict['data']['upper']['mid'])
        add_sub_comment(all_comments,current_up_id)
        
    
    
def main():
    filepath='.\Bilibili'
    filename_list=listdir(filepath)
    h=[]   
        #可以同过简单后缀名判断，筛选出你所需要的文件(这里以.json为例)
    for filename in filename_list:#依次读入列表中的内容
        if filename.endswith('json'):
            if '完整' in filename:# 后缀名'json'匹对
                h.append(filename)#如果是'json'文件就添加进列表h
            elif '简略' in filename and filename.replace('简略','完整') not in h:
                h.append(filename)
    print(h)
    print(len(h))
    time.sleep(0.5)
    #add_comment(h[0])
    pool = mp.Pool(processes=20)
    pool.map(add_comment,h)
    pool.close()
    pool.join()              
if __name__=='__main__':
    main()
