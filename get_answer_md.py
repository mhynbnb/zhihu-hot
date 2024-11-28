import random
import os
import requests
import pandas as pd
import time
from bs4 import BeautifulSoup
import datetime

def sparser_list():
	hot_list=[]
	with open(f'hot_list{datetime.date.today()}.txt', 'r',encoding='utf-8') as f:
		lines=f.readlines()
		for line in lines:
			title,hot,url,image_url,content=line.split('||')
			hot_list.append([title,hot,url,image_url,content,url.split('/')[-1]])
	return hot_list

def get_answer_content(title,hot,content,question_id,cookies,answer_page_num):

	template = 'https://www.zhihu.com/api/v4/questions/{question_id}/feeds?cursor=1c4cacd45e70f24bd620bad51c605d59&include=data[*].is_normal,admin_closed_comment,reward_info,is_collapsed,annotation_action,annotation_detail,collapse_reason,is_sticky,collapsed_by,suggest_edit,comment_count,can_comment,content,editable_content,attachment,voteup_count,reshipment_settings,comment_permission,created_time,updated_time,review_info,relevant_info,question,excerpt,is_labeled,paid_info,paid_info_content,reaction_instruction,relationship.is_authorized,is_author,voting,is_thanked,is_nothelp;data[*].mark_infos[*].url;data[*].author.follower_count,vip_info,badge[*].topics;data[*].settings.table_of_content.enabled&limit=5&{offset}&order=default&platform=desktop&session_id=1698132896804376037'

	answer_ids = []
	headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'}
	cookies = {'cookie': cookies}

	url0 = template.format(offset=0,question_id=question_id)
	resp0 = requests.get(url0, headers=headers, cookies=cookies)
	for data in resp0.json()['data']:
		answer_id = data['target']['id']  # 添加answer_id到df中
		answer_ids.append(answer_id)
	next = resp0.json()['paging']['next']
	print(f'[{title}]'.center(50, ' '))
	dir_name=title.split(':')[0]

	print('获取answerid'.center(50,'='))
	for page in range(1, answer_page_num+1):  # 这里自己估算一下，每页是5条数据
		resp = requests.get(next, headers=headers, cookies=cookies)
		# print('正在爬取第' + str(page) + '页')
		for data in resp.json()['data']:
			answer_id = data['target']['id']
			voteup_count=data['target']['voteup_count']
			name=data['target']['author']['name']
			# 添加answer_id到df中
			# print(data)
			answer_ids.append([answer_id,voteup_count,name])
			print(answer_id, voteup_count,name)
		next = resp.json()['paging']['next']
		time.sleep(1)
	# print(answer_ids)

	print('获取answer数据'.center(50, '='))
	contents = f'## {title}\n{content}\n**{hot}**\n'
	img_urls = []
	count = 1
	os.makedirs(f'content', exist_ok=True)
	os.makedirs(f'content/{dir_name}', exist_ok=True)
	os.makedirs(f'content/{dir_name}/image', exist_ok=True)

	with open(f'content/{dir_name}/answer.md', 'w', encoding='utf-8') as f:
		for answer in answer_ids:
			answer_id = answer[0]
			contents += f'### {answer[2]}\n*{answer[1]}人赞同*\n'

			print(f'正在爬取answer_id为{answer_id}的数据')
			url = f'https://www.zhihu.com/question/{question_id}/answer/{answer_id}'
			resp = requests.get(url, headers=headers, cookies=cookies)
			soup = BeautifulSoup(resp.text, 'html.parser')

			content = soup.find('div', class_='RichContent-inner')
			# print(content)
			content_list = content.find_all(['p','img','code'])
			for c in content_list:
				if c.name=='p':
					if c.text !='':
						contents += c.text+'\n'
					# print('p')
				elif c.name=='img':
					# print('img')
					if len(c['class']) == 2:
						if c['class'][0] == 'origin_image':
							# print(img['data-original'])
							img_content = requests.get(c['data-original'], headers=headers, cookies=cookies).content
							with open(f'content/{dir_name}/image/{count}.jpg', 'wb') as f1:
								f1.write(img_content)
								img_urls.append(f'image/{count}.jpg')
								count += 1
							contents+=f'![](image/{count}.jpg)\n'
						elif c['class'][0] == 'content_image':
							img_content = requests.get(c['data-actualsrc'], headers=headers, cookies=cookies).content
							with open(f'content/{dir_name}/image/{count}.jpg', 'wb') as f1:
								f1.write(img_content)
								img_urls.append(f'image/{count}.jpg')
								contents += f'![](image/{count}.jpg)\n'
								count += 1
				elif c.name=='code':
					contents += '```text\n'+c.text + '\n```\n'

		f.write(contents)