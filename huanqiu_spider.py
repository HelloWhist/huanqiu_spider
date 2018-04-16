# coding: utf-8
import requests
import sys
from bs4 import BeautifulSoup as bs

def get_content(url):
    data = {}
    r = requests.get(url)
    r.encoding = 'utf-8'
    soup = bs(r.text,'lxml')
    title = soup.title.string.strip(' _军事_环球网') # title
    kw = soup.find_all('meta')[2]['content']  # keywords
    des = soup.find_all('meta')[3]['content']  # description
    source = soup.select('.l_a > .la_tool > .la_t_b > a')[0].string
    time = soup.select('.l_a > .la_tool > .la_t_a')[0].string
    data = {
        'url':url,
        'title':title,
        'keywords':kw,
        'description':des,
        'source':source,
        'time':time
    }
    print(data)
    paras = soup.select('.l_a > .la_con')[0].find_all('p')
    fo = open('news.txt',"w+")
    for para in paras:
        if len(para) > 0 and para.string != None:
            fo.writelines(para.string.strip() + "\n")
    fo.close()
    
    try:
        img_url = soup.select('.l_a > .la_con > p > img')[0]['src']
        img_res = requests.get(img_url,stream=True)
        img_name = "news.jpg"
        with open(img_name,"wb") as f:
            for chunk in img_res:
                f.write(chunk)
    except Exception:
        print("This article doesn't have pictures.")
        # print(Exception) <class 'Exception'>
        
if __name__ == "__main__":
    # print(type(sys.argv[1:]))   # It's a list
    get_content(sys.argv[1:][0])
