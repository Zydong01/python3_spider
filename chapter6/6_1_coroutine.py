import asyncio
import time
import requests
import aiohttp

startTime = time.time()
print(startTime)

async def getUrl(url):
    session = aiohttp.ClientSession()
    response = await session.get(url)
    await response.text()
    await session.close()
    return response

# 协程
async def request():
    url = "http://www.httpbin.org/delay/5"
    r = await getUrl(url)

tasks = [asyncio.ensure_future(request()) for _ in range(1000)]

loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait(tasks))

endTime = time.time()
print(endTime)
print("花费时间：",endTime-startTime)