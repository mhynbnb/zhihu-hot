'''
File : get_answer_md.py
Auther : MHY
Created : 2024/11/28 13:07
Last Updated :
Description :
Version :
'''
import time
from ebooklib import epub
from get_hot_list import get_hot_list
from  get_answer_md import get_answer_content,sparser_list
cookies=''
print('获取热榜列表'.center(50, '='))
get_hot_list()
print('开始爬取数据'.center(50, '='))
hot_list=sparser_list()
answer_page_num=2#一页为5个回答
for hot in hot_list[:]:
	title,hot,url,image_url,content,question_id=hot
	get_answer_content(title,hot,content,question_id,cookies,answer_page_num)
	time.sleep(2)
	print(f'[{title}] 搞定！')
