import urllib.request
import urllib.parse
import json
import time
from lxml import etree

url = 'https://www.amazon.ca/s?k=goalkeeper+gloves&language=fr&crid=5B0S4SQ1GOGS&qid=1661147954&sprefix=goa%2Caps%2C157&ref=sr_pg_'
headers = {'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Mobile Safari/537.36'}

for i in range(7):
    new_url = url + str(i+1)
    request = urllib.request.Request(url=new_url,headers=headers)
    data = {'http':'175.7.199.100:3256'}
    handler = urllib.request.ProxyHandler(proxies=data)
    opener = urllib.request.build_opener(handler)
    response = opener.open(request)
    content = response.read().decode('utf-8')
    tree = etree.HTML(content)
    src = tree.xpath('//*[@id="search"]//img/@src')
    print(len(src))
    for i in range(len(src)) :
        s1 = src[i]



    # fp = open('amazon'+str(i+10)+'.json','w',encoding='utf-8')
    # fp.write(content)


