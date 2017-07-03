#!/usr/bin/env python3

import urllib.request
from bs4 import BeautifulSoup

_help = """Usage: {} [OPTION] ... [URL] ...
"""

def crawl_pages(pages):
    content_array = []
    for p in pages:
        c = urllib.request.urlopen(p).read().decode('gbk')
        content_array.append(c)
    return content_array

def parse_xunsee(url):
    print("parsing xunsee!")
    split = url.rsplit('/', 1) # cut into directory/page
    content = urllib.request.urlopen(url).read().decode('gbk')
    soup = BeautifulSoup(content, 'lxml').find_all(id="content_1")
    spants = soup[0].find_all('span')
    pages = list(map(lambda x: x.find_all('a')[0].get('href'), spants))
    pages = list(map(lambda x: split[0] + '/' + x, pages))
    # crawl only first five pages
    pages = pages[:2]
    content_array = crawl_pages(pages)
    for c in content_array:
        print(c)

def main(**kwargs):
    url = kwargs['url']
    if "xunsee" in url.lower():
        parse_xunsee(url)
    
if __name__ == '__main__':
    main()
