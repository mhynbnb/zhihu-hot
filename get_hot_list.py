'''
File : get_hot_list.py
Auther : MHY
Created : 2024/11/28 14:52
Last Updated : 
Description : 
Version : 
'''

from bs4 import BeautifulSoup
import requests
import json
import datetime
def get_hot_list():
    headers = {'scheme': 'https',
               'accept': 'text/html, application/xhtml+xml, application/xml',
               'accept-language': 'zh-CN, zh',
               'user-agent': 'Mozilla/5.0 (Windows NT 10.0 Win64 x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36'
               }

    r = requests.get('https://www.zhihu.com/billboard', headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    data = json.loads(soup.find('script', {'id': 'js-initialData'}).get_text())
    jsonStr = data['initialState']['topstory']['hotList']

    textStr = ''
    for index, item in enumerate(jsonStr):
        # print(item['target'])
        titleArea = item['target']['titleArea']['text']
        excerptArea = item['target']['excerptArea']['text']
        imageArea = item['target']['imageArea']['url']
        metricsArea = item['target']['metricsArea']['text']
        link = item['target']['link']['url']
        itemStr = '{:02d}:{}||{}||{}||{}||{}'.format(
            index+1,  titleArea, metricsArea, link, imageArea, excerptArea)
        # print(itemStr)
        print(index+1,  titleArea)
        textStr += itemStr+'\n'
        # print(item['target']['excerptArea'])
    with open(f'hot_list{datetime.date.today()}.txt', 'w', encoding="utf-8") as f:
        f.write(textStr)

if __name__ == '__main__':
    get_hot_list()