# 1.注意r.text和r.json()的区别使用 返回网页源代码使用r.text，返回ajax中的json数据，使用r.json
# 2.str.format的使用，用来拼接字符串
# 这个例子中没有页面解析的操作，仅仅是分析url以及对应的ajax数据url，直接获得json数据


import requests
import multiprocessing
import time

INDEX_URL = 'https://spa1.scrape.center/api/movie/?limit={limit}&offset={offset}'
DETAIL_URL = 'https://spa1.scrape.center/api/movie/{id}/'

# 爬取ajax页面的json数据
def scrape_json(url):
    try:
        r = requests.get(url)
        print(r.status_code)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.json()
    except:
        print('爬取失败')

# 爬取列表页面的数据
def get_index_text(page):
    limit = 10
    url = INDEX_URL.format(limit=10, offset=limit * (page-1))
    return scrape_json(url)

# 爬取详情页面的数据
def get_detail_text(id):
    url = DETAIL_URL.format(id=id)
    return scrape_json(url)


# def main():
#     start = time.time()
#     for i in range(1, 11):
#         index_data = get_index_text(i)
#         for item in index_data.get('results'):
#             id = item.get('id')
#             print(id)
#             print(get_detail_text(id))
#     end = time.time()
#     print("用时：", end - start)
#
# main()

def main(pageNum):
    index_data = get_index_text(pageNum)
    for item in index_data.get('results'):
        id = item.get('id')
        print(get_detail_text(id))

if __name__ == '__main__':
    pool = multiprocessing.Pool()
    pagesNum = range(1, 11)
    start = time.time()
    pool.map(main, pagesNum)
    pool.close()
    pool.join()
    end = time.time()
    print("用时：",end-start)