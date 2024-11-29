'''
File : get_answer_md.py
Auther : MHY
Created : 2024/11/28 13:07
Last Updated :
Description :
Version :
'''
import os
import cv2
import time
from ebooklib import epub
from get_hot_list import get_hot_list
from  get_answer_epub import get_answer_content,sparser_list


def resize_image(input_path, output_path, scale_factor):
	"""
	按比例缩放图像并覆盖原文件
	:param input_path: 输入图像路径
	:param output_path: 输出图像路径（可以与输入路径相同以覆盖原文件）
	:param scale_factor: 缩放比例（例如：0.5 表示缩小一半）
	"""
	# print(input_path)
	img = cv2.imread(input_path)
	new_width = int(img.shape[1] * scale_factor)
	new_height = int(img.shape[0] * scale_factor)
	resized_img = cv2.resize(img, (new_width, new_height))
	cv2.imwrite(output_path, resized_img)


'''填写自己的cookie'''
cookies=''
print('获取热榜列表'.center(50, '='))
get_hot_list()
print('开始爬取数据'.center(50, '='))
hot_list=sparser_list()
answer_page_num=2#一页为5个回答
book = epub.EpubBook()
book.set_title('知乎热榜')
book.set_language('zh')
book.add_author('MHY')
# cover_image_path = 'cover.png'
# cover_image = open(cover_image_path, 'rb').read()
# book.set_cover('cover.png', cover_image)
toc=[]
spine=['nav']
chapter_num=0

for hot in hot_list[:]:
	title,hot,url,image_url,content,question_id=hot
	contents=get_answer_content(title,hot,content,question_id,cookies,answer_page_num)
	time.sleep(2)
	print(f'[{title}] 搞定！')

	chapter_num += 1
	c1 = epub.EpubHtml(title=f'{title}', file_name=f'chap_{chapter_num}.xhtml', lang='zh')
	c1.content = contents
	book.add_item(c1)
	# toc.append(c1)
	toc.append(epub.Link(f'chap_{chapter_num}.xhtml', f'{title}', f'chap_{chapter_num}'), )
	print(f'{chapter_num:02d} {title}')
	spine.append(c1)
for image_path in os.listdir('content_epub/image'):
	# print(image_path)
	try:
		resize_image('content_epub/image/'+image_path, 'content_epub/image/'+image_path, 0.5)#可选，缩放图片
	except:
		pass
	with open('content_epub/image/'+image_path, 'rb') as image_file:
		img = image_file.read()
	book.add_item(epub.EpubImage(file_name=f'image/{image_path}', media_type='image/jpeg', content=img))

book.add_item(epub.EpubNcx())
book.add_item(epub.EpubNav())
book.toc = toc
book.spine =spine
epub.write_epub('content_epub/知乎热榜.epub', book, {})
