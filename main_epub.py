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
cookies='SESSIONID=jiZZezjcptDyYMoDofGRaW2tYPkBmPKtxCNvdS8EUZy; JOID=WlEQBE_ZPobpMlxpNtYzXoHAmBssu2D9rlsqH0WXXOPaXBkcC6bLwIE_UWc3jywxAqNTB9e5pcct-UEWVShnsdg=; osd=W1gUC0jYN4LmNV1gMtk0X4jElxwtsmTyqVojG0qQXereUx4dAqLEx4A2VWgwjiU1DaRSDtO2osYk_U4RVCFjvt8=; YD00517437729195%3AWM_TID=mhzpJJI2fo5BAREAUEPBjO%2F5qFNYHSQH; YD00517437729195%3AWM_NI=pCIIrtHjdeUSHEEg9Sa87t49bg16Szu2jPql3e2zz8qECOkmPK5M98XzDAvZZ4XIp1shOX4XzjPeG3esVCcO14eimuWeClfrRWcX4U96zemYcL4s8lvPhrumUgztbbrNWTM%3D; YD00517437729195%3AWM_NIKE=9ca17ae2e6ffcda170e2e6eeb8f368fc9da5d3d37396968ba2d14e879e8b82c162aeaa8990e972f1f1a5d3d92af0fea7c3b92ab49d87aaf1808cb6ac86d8598c9b8b88bc59a3e8f995b733a2b9ffd7d272b7eea6b1f468f1bbfe9bf934b39b8db0ea679495fbaebc349ca68ca2f5529aec98aaf33bb1b881b9b754bab6a086c639a7ad9aa4e245f3ecab8af07f95bb8d8de57a9289adb9b75ffbeab686f053a194fc94bb68b690a893f86797b9b695e16ab29299b5d037e2a3; q_c1=eca0e1738eed4a3da9683880abd7002e|1698569604000|1698569604000; _xsrf=f7dR64YkBc7lXGP1BJvbhLdxDBpcA9wy; ISSW=1; q_c1=eca0e1738eed4a3da9683880abd7002e|1727663659000|1698569604000; __utma=51854390.2131328259.1727663661.1727663661.1727663661.1; __utmz=51854390.1727663661.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmv=51854390.100-1|2=registration_date=20181212=1^3=entry_date=20181212=1; _ga=GA1.2.2131328259.1727663661; _ga_MKN1TB7ZML=GS1.2.1730364370.1.1.1730364432.0.0.0; _zap=db08f42e-b110-4bed-bc3c-5c0ce0e404c8; d_c0=AGDS4P1ugRmPThzGojNdKf3WGvmj6Lbb7sM=|1730962868; z_c0=2|1:0|10:1731993247|4:z_c0|80:MS4xcHUtRkRRQUFBQUFtQUFBQVlBSlZUWjVzS1dnbkZ3NFNjaU5jWHUwNVhIZzYwWjhwVzRXQUNBPT0=|ee042c144bdd9c69408911c6655252a8ab3ca1486adc22d983951b5520adb522; __zse_ck=003_bs0VzXmlSygFW3aQjVntVwVH0G/Vu3PYeO=yz4JgDtiYEUXQy9MW2SeMXCYs=TsJorWRx55wlLAkLiDuGD5pGajg1x9SMFIMA+p8Wg3RD=hS; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1732186188,1732518505,1732612060,1732769277; HMACCOUNT=6C57B6E12D54B2E9; tst=h; ff_supports_webp=1; SESSIONID=cRyDewzqBci1mIt1jg3Dwg8akaHbzA5l4CBxu5ofJdd; JOID=V1oVCkM9xmIfVANlJzHMsnKvxBA1WZYSWjxzHV9yogknOEcWFOc0LXReBm4vUCuJNRNWzek2-f6TVB00qhcYVOM=; osd=V1wUAkg9wGMXXwNjJjnHsnSuzBs1X5caUTx1HFd5og8mMEwWEuY8JnRYB2YkUC2IPRhWy-g-8v6VVRU_qhEZXOg=; BEC=4589376d83fd47c9203681b16177ae43; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1732770673'
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