# coding: utf-8
import requests
import sys

import os
from bs4 import BeautifulSoup as bs

IMG_DIR = "./img/"
IMG_URL = "img/%s"
data = {}

if not os.path.exists(IMG_DIR):
    os.mkdir(IMG_DIR)

def get_content(url):
    r = requests.get(url)
    r.encoding = 'utf-8'
    soup = bs(r.text,'lxml')
    title = soup.select('.l_a > h1')[0].string# title
    keywords = soup.find('meta',{'name':'keywords'})['content']# keywords
    des = soup.find('meta',{'name':'description'})['content']
    source = soup.select('.l_a > div.la_tool > span.la_t_b')[0].string.strip()
    time = soup.select('.l_a > div.la_tool > span.la_t_a')[0].string
        
    body_content = soup.find('div', {'class': 'la_con'})
    p_list = []
    for i, p in enumerate(body_content.find_all('p')):
        if p.attrs is not None:
            del p.attrs

        img_lists = p.find_all('img')
        for img in img_lists:
            img_url = img["src"]
            img_name = img_url.split("/")[-1]
            nr = requests.get(img_url, stream=True)
            with open(os.path.join(IMG_DIR, img_name), "wb") as f:
                for chunk in nr.iter_content(chunk_size=512):
                    f.write(chunk)
            img["src"] = IMG_URL % img_name
        p_list.append(str(p))
    content = "\n".join(p_list)  
    
    ##save in a text file
    news_name = "%s.txt" % title[:5]
    with open(news_name,"w+",encoding='utf-8') as f:
        f.write(title + '\n')
        f.write(keywords + '\n')
        f.write(des + '\n')
        f.write(source + '\n')
        f.write(time + '\n')
        f.write(content)
    
if __name__ == "__main__":
    get_content(sys.argv[1])