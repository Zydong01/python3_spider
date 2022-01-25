import re
import time
import requests
import asyncio
import aiohttp

# 运行失败，不知道有没有通过协程加快速度，并且通过session得到的r.text不是string类型，无法对网页进行提取
async def get(url):
    session = aiohttp.ClientSession()
    r = await session.get(url)
    await r.text()
    await session.close()
    return r

async def getHtml(url):
    try:
        r = await get(url)
        # r.raise_for_status()
        # r.encoding = r.apparent_encoding
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
    loop = asyncio.get_event_loop()
    for i in range(1, 11):
        coroutine = getHtml(url+"page/"+str(i))
        task = asyncio.ensure_future(coroutine)
        loop.run_until_complete(task)
        # html = html + getHtml(url+"page/"+str(i))
    getMovieList(html)
    endTime = time.time()
    print("总用时：", endTime-startTime)

main()
