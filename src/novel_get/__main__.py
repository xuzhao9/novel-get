#!/usr/bin/env python3

import urllib.request
from bs4 import BeautifulSoup

_help = """Usage: {} [OPTION] ... [URL] ...
"""

def crawl_pages(pages):
    content_array = []
    for idx, p in enumerate(pages):
        print("Crawling " + idx + "/" + len(pages))
        c = urllib.request.urlopen(p).read().decode('gbk')
        content_array.append(c)
    return content_array

def parse_xunsee(url, ofile):
    split = url.rsplit('/', 1) # cut into directory/page
    content = urllib.request.urlopen(url).read().decode('gbk')
    soup = BeautifulSoup(content, 'lxml').find_all(id="content_1")
    spants = soup[0].find_all('span')
    pages = list(map(lambda x: x.find_all('a')[0].get('href'), spants))
    pages = list(map(lambda x: split[0] + '/' + x, pages))
    # crawl only first five pages
    # pages = pages[:2]
    content_array = crawl_pages(pages)
    article_array = []
    for idx, c in enumerate(content_array):
        csoup = BeautifulSoup(c, 'lxml').find(id="content_1")
        article = csoup.get_text().strip().replace("　　", "　")\
                                          .replace("上一页  目录  下一页", "")\
                                          .replace("目录  下一页", "")
        article_array.append(article)
    out = '\n'.join(article_array)
    dumper(out, ofile)

# convert novel to txt file
def dumper(novel, ofile):
    if ofile.endswith(".txt"):
        print("Dumping txt...")
        out = open(ofile, 'w')
        out.write(novel)
        out.close()
    elif ofile.endswith(".pdf"):
        print("Dumping pdf...")
    else:
        print("Only txt and pdf formats are supported!")

def main(**kwargs):
    url = kwargs['url']
    out = kwargs['out']
    if "xunsee" in url.lower():
        parse_xunsee(url, out)
    
if __name__ == '__main__':
    main()
