# -*- coding: utf-8 -*-
"""
Created on Mon Apr  2 15:53:12 2018

@author: Administrator
"""
import pandas as pd
def main():
    df=pd.read_excel('up_video_info.xlsx')
    av_id=list(df['av'])
    av_id.sort()
    print(len(av_id))
    with open('哔哩哔哩AV号.txt','a+') as f:
        for item in av_id:
            f.write(str(item)+'\n')

if __name__=='__main__':
    main()