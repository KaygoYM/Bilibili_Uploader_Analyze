# -*- coding: utf-8 -*-
"""
Created on Wed Mar 28 14:17:29 2018

@author: Administrator
"""

# -*-coding:utf8-*-

import requests
import json
import random
import time
import pandas as pd

def UserAgent():
    user_agents = []
    with open('user_agents.txt') as f:
        for lines in f.readlines():
            user_agents.append(lines.strip()[1:-1])
    return user_agents

def request_data(user_agents,mid):
    userAgent=random.choice(user_agents)
    base_url='https://space.bilibili.com/ajax/member/GetInfo'
    
    proxies = {
        'http': 'http://61.155.164.108:3128',
        'http': 'http://116.199.115.79:80',
        'http': 'http://42.245.252.35:80',
        'http': 'http://106.14.51.145:8118',
        'http': 'http://116.199.115.78:80',
        'http': 'http://123.147.165.143:8080',
        'http': 'http://58.62.86.216:9999',
        'http': 'http://202.201.3.121:3128',
        'http': 'http://119.29.201.134:808',
        'http': 'http://61.155.164.112:3128',
        'http': 'http://123.57.76.102:80',
        'http': 'http://116.199.115.78:80',
    }
    
    headers={
        'Accept':'*/*',
        'Accept-Encoding':'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Connection':'keep-alive',
        'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
        'User-Agent':userAgent,
        'Origin':'http://space.bilibili.com',
        'Referer': 'http://space.bilibili.com/%s' % mid,
        'X-Requested-With': 'XMLHttpRequest',
    }
    payload={'mid':str(mid),'csrf':'null'}#,'_': datetime_to_timestamp_in_milliseconds(datetime.datetime.now())}
    try:
        r=requests.post(base_url,headers=headers,data=payload,proxies=proxies)
        print(r)
        if r.status_code==200:
            r=r.text
    except Exception as err:
        print(err)
        pass
    time.sleep(random.randint(1,3))
    return json.loads(r)

def handle_data(data,item):
    if data['status']==True:
        data=data['data']
        #print(data)
        item['article'].append(data['article'])#文章数
        item['mid'].append(data['mid'])#用户ID
        if '=' in data['name']:
            temp=data['name'].replace('=','')
            item['name'].append(temp) #用户昵称
        else:
            item['name'].append(data['name'])
        item['sex'].append(data['sex'] if data['sex']!='' else 'None')#用户性别
        item['coins'].append(data['coins'])#用户B币数
        try:
            item['birthday'].append(data['birthday'])#生日
        except:
            item['birthday'].append('None')
        try:
            item['place'].append(data['place'] if data['place']!=''  else 'None')#注册地
        except:
            item['place'].append('None')
        item['playnum'].append(data['playNum'])#播放量
        item['sign'].append(data['sign'] if data['sign'] else 'None')#用户简介
        item['currentlevel'].append(data['level_info']['current_level'])#用户当前等级
        try:
            regtime=time.localtime(data['regtime'])
            regtime=time.strftime('%Y-%m-%d',regtime)
            item['regtime'].append(regtime)#用户注册时间
        except:
            item['regtime'].append('None')
        item['vip'].append(data['vip']['vipStatus'])#VIP标识
        time_local = time.localtime(time.time())
        #转换成新的时间格式(2016-05-05 20:28:54)
        part_date= time.strftime("%Y-%m-%d %H:%M:%S",time_local)
        item['part_date'].append(part_date)
        #print(item)
        #follower_num and following_num
        res = requests.get('https://api.bilibili.com/x/relation/stat?vmid='+str(data['mid'])+'&jsonp=jsonp&').text
        js_fans_data = json.loads(res)
        following = js_fans_data['data']['following']
        fans = js_fans_data['data']['follower']
        item['following_num'].append(following)
        item['fans_num'].append(fans)
    else:
        print('no data now')
'''
{'mid': '423895', 'name': '怕上火暴王老菊', 'approve': False, 'sex': '保密', 'rank': '10000', 
'face': 'http://i2.hdslb.com/bfs/face/2edf4a4f534869a63158d13a4b6b9676d75f1e0a.jpg', 'DisplayRank': '1043', 
'regtime': 1339205465, 'spacesta': 0, 'birthday': '0000-03-22', 'place': '', 
'description': '', 'article': 0, 'sign': 'weibo.com/573244552', 
'level_info': {'current_level': 6, 'current_min': 28800, 'current_exp': 2736194, 'next_exp': -1},
'pendant': {'pid': 5, 'name': '哔哩王', 'image': 'http://i1.hdslb.com/bfs/face/67ed957ae789852bcc59b1c1e3097ea23179f793.png', 'expire': 1534609110}, 
'nameplate': {'nid': 1, 'name': '黄金殿堂', 'image': 'http://i2.hdslb.com/bfs/face/82896ff40fcb4e7c7259cb98056975830cb55695.png', 
'image_small': 'http://i1.hdslb.com/bfs/face/627e342851dfda6fe7380c2fa0cbd7fae2e61533.png', 
'level': '稀有勋章', 'condition': '单个自制视频总播放数>=100万'}, 'official_verify': {'type': -1, 'desc': ''}, 
'vip': {'vipType': 2, 'vipDueDate': 1566057600000, 'dueRemark': '', 'accessStatus': 1, 'vipStatus': 1, 'vipStatusWarn': ''},
'toutu': 'bfs/space/cfa83574e55de044a91b410ea9dd324a6bb7012f.png', 'toutuId': 216745, 'theme': 'default', 'theme_preview': '', 
'coins': 0, 'im9_sign': '7224901eb5b4f421ca801ec6c3cd494a', 'playNum': 195753394, 'fans_badge': True}
'''

def main():
    writer=pd.ExcelWriter('output_up.xlsx')
    #mid_list=['00','10','7349','808171','423895']
    mid_list=['808171','7349','423895','122879','883968','168598','419220','116683','119418','927587','8578857','4162287','777536','43536','51766','1532165','14110780'
              ,'282994','11073']#你要的up主都在这里了
    global dict_whole
    dict_whole={'article':[],'mid':[],'name':[],'sex':[],
                'coins':[],'birthday':[],'place':[],'playnum':[],
                'sign':[],'currentlevel':[],'regtime':[],'vip':[],
                'following_num':[],'fans_num':[],'part_date':[]}
    for mid in mid_list:
        try:
            jsdata=request_data(UserAgent(),mid)
            handle_data(jsdata,dict_whole)
        except:
            continue        
    df=pd.DataFrame(dict_whole)
    df.to_excel(writer,index=False)
    writer.save()

if __name__=='__main__':
    main()
