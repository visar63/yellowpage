import scrapy
import re
import pyodbc
import requests
import gzip
import time
from io import BytesIO
import time

s  = requests.Session()
user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
s.headers.update({
    'user-agent':user_agent,
})

# proxy_ = "http://35.231.78.58:80"
# s.proxies = {
#     'http':proxy_,
#     'https':proxy_
# }

url = "https://www.yellowpages.ca/sitemap.xml"

r = s.get(url)


if r.status_code == 200:
    print (r.url)
    #print (r.text)

for link in re.findall(r'<loc>(https://www.yellowpages.ca/sitemap/en/merchant.*?)</loc>',str(r.text),re.I|re.S):               
    response = s.get(url=link, timeout = 300)
    if response.status_code == 200:
        time.sleep(10)
        print('Link: %s' % link)
        out = BytesIO(response.content)
        with gzip.open(out,mode='r') as f:
            with open('links2.txt','at') as a:
                for line in f.readlines():
                    pattern = re.search(r'<loc>([^<]+)</loc>',line.decode('utf-8'))
                    if pattern:
                        link = pattern.group(1)                                        
                        a.write(link + '\n')