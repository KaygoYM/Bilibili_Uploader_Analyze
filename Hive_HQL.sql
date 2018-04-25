--交集粉丝(弹幕版)
select av_stn.sender_id,av_stn.danmu_num,av_lion.danmu_num from
(select sender_id,count(content) as danmu_num from temp.bilibili_danmu where bilibili_danmu.av in
(select av from temp.bilibili_video where up_name='STN工作室')
group by sender_id)av_stn
join
(select sender_id,count(content) as danmu_num from temp.bilibili_danmu where bilibili_danmu.av in
(select av from temp.bilibili_video where up_name='吃素的狮子')
group by sender_id)av_lion
on av_stn.sender_id=av_lion.sender_id

--交集粉丝(评论版)
select av_stn.user_id,av_stn.user_name,av_stn.comment_num,av_lion.comment_num from
(select user_id,user_name,count(comment) as comment_num from temp.bilibili_comment_stn_lion where up_id=7349 and user_id!=7349 group by user_id,user_name)av_stn
join
(select user_id,user_name,count(comment) as comment_num from temp.bilibili_comment_stn_lion where up_id=808171 and user_id!=808171 group by user_id,user_name)av_lion
on av_stn.user_id=av_lion.user_id


--各up主表现
select up_name,avg(play_num) as avg_play_num,avg(danmu_num) as avg_danmu_num,avg(coin_num) as avg_coin_num,avg(favorite_num) as avg_favorite_num ,avg(comment_num) as avg_comment_num,
count(av) as av_amount from temp.bilibili_video
where substr(time,7,1)>='2017-04'
group by up_name

--抽弹幕做词云（史蛋为例）
select content from temp.bilibili_danmu where bilibili_danmu.av in
(select av from temp.bilibili_video where up_name='STN工作室' and substr(time,7,1)>='2017-04')