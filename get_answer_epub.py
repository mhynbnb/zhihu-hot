import random
import os
import requests
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
	print('获取answerid'.center(50,'='))
	for page in range(1, answer_page_num+1):
		resp = requests.get(next, headers=headers, cookies=cookies)
		for data in resp.json()['data']:
			answer_id = data['target']['id']
			voteup_count=data['target']['voteup_count']
			name=data['target']['author']['name']
			answer_ids.append([answer_id,voteup_count,name])
			print(answer_id, voteup_count,name)
		next = resp.json()['paging']['next']
		time.sleep(1)


	print('获取answer数据'.center(50, '='))
	contents = f'<h1>{title}</h1><p>{content}</p><p><b>{hot}</b></p>'
	img_urls = []
	count = 1
	os.makedirs(f'content_epub', exist_ok=True)
	os.makedirs(f'content_epub/image', exist_ok=True)
	# os.makedirs(f'content/{dir_name}/image', exist_ok=True)

	# with open(f'content/{dir_name}/answer.md', 'w', encoding='utf-8') as f:
	for answer in answer_ids:
		answer_id = answer[0]
		contents += f'<h2>{answer[2]}<h2><p><i>{answer[1]}人赞同</i></p>'

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
					contents += '<p>'+c.text+'</p>'
				# print('p')
			elif c.name=='img':
				# print('img')
				if len(c['class']) == 2:
					if c['class'][0] == 'origin_image':
						# print(img['data-original'])
						img_content = requests.get(c['data-original'], headers=headers, cookies=cookies).content
						with open(f'content_epub/image/{question_id}_{count}.jpg', 'wb') as f1:
							f1.write(img_content)
							img_urls.append(f'image/{question_id}_{count}.jpg')
							count += 1
						contents+=f'<div style="text-align: center;"><img src="image/{question_id}_{count}.jpg" width="500"></div>'
					elif c['class'][0] == 'content_image':
						img_content = requests.get(c['data-actualsrc'], headers=headers, cookies=cookies).content
						with open(f'content_epub/image/{question_id}_{count}.jpg', 'wb') as f1:
							f1.write(img_content)
							img_urls.append(f'image/{question_id}_{count}.jpg')
							contents+=f'<div style="text-align: center;"><img src="image/{question_id}_{count}.jpg" width="500"></div>'
							count += 1
			elif c.name=='code':
				contents += '<p>'+c.text + '</p>'
		time.sleep(1)
	return contents