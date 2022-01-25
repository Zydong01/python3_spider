import re
import time
import requests

# 获取了所有电影名称
def getHtml(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        print("获取网页失败")

def getMovieList(html):
    movieNames = re.findall('m-b-sm">(.*?)</h2>', html, re.S)
    print(movieNames, len(movieNames))
    pass

def main():
    url = "https://ssr1.scrape.center/"
    html = ""
    startTime = time.time()
    for i in range(1, 11):
        html = html + getHtml(url+"page/"+str(i))
    getMovieList(html)
    endTime = time.time()
    print("总用时：", endTime-startTime)

main()
