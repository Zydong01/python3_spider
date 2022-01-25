# 爬取思路：首先爬取所需的全部页面，然后再爬取页面总所需要的信息，由浅入深的写代码
# 并不是所有的页面都需要爬取，比如列表页的内容在详情页里都有，只需爬取详情页即可

import requests
import re
import time
import logging

from os.path import exists
from os import makedirs
import json

import multiprocessing

# 全局变量提前定义好
BASE_URL = "https://ssr1.scrape.center"
TOTAL_PAGE = 10
RESULTS_DIR = 'F:/result'
exists(RESULTS_DIR) or makedirs(RESULTS_DIR)

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s: %(message)s')


# 爬取一个页面的通用方法
# 传入一个url，返回页面html文本
def scrape_page(url):
    logging.info('scraping %s...', url)
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
        logging.error('get invalid status code %s while scraping %s', response.status_code, url)
    except:
        logging.error('error occurred while scraping %s', url, exc_info=True)


# 爬取列表页
# 传入页码，返回该页码页面的html文本
def scrape_index(pageNum):
    return scrape_page(BASE_URL + "/page/" + str(pageNum))


# 解析列表页获取详情页url
# 传入列表页文本，返回文本中详情页url
def parse_index(html):
    part_url = re.findall('<a.*?href="(.*?)".*? class="name">', html)
    logging.info('get detail url %s', part_url)
    return part_url
    # print(part_url)


# 爬取详情页
# 传入一个详情页url，返回详情页html文本
def scrape_detail(partUrl):
    url = BASE_URL + partUrl
    Html = scrape_page(url)
    return Html


# 解析详情页
# 传入html文本，解析获得相应的信息，通过字典形式返回
def parse_detail(html):
    cover_pattern = re.compile('class="item.*?<img.*?src="(.*?)".*?class="cover">', re.S)
    cover = re.search(cover_pattern, html).group(1).strip() if re.search(cover_pattern, html) else None

    name_pattern = re.compile('<h2.*?>(.*?)</h2>', re.S)
    name = re.search(name_pattern, html).group(1).strip() if re.search(name_pattern, html) else None

    categories_pattern = re.compile('<button.*?186.*?<span>(.*?)</span>', re.S)
    categories = re.findall(categories_pattern, html) if re.findall(categories_pattern, html) else None

    publish_pattern = re.compile('(\d{4}-\d{2}-\d{2})')
    publish = re.search(publish_pattern, html).group(1).strip() if re.search(publish_pattern, html) else None

    drama_pattern = re.compile('<div.*?drama.*?<p.*?>(.*?)</p>', re.S)
    drama = re.search(drama_pattern, html).group(1).strip() if re.search(drama_pattern, html) else None

    score_pattern = re.compile('score.*?>(.*?)</p>', re.S)
    score = re.search(score_pattern, html).group(1).strip() if re.search(score_pattern, html) else None
    dic = {
        'cover': cover,
        'name': name,
        'categories': categories,
        'publish': publish,
        'drama': drama,
        'score': score
    }
    return dic


# 将爬取的内容以json数据的形式存储在本地文件夹中
def save_data(data):
    name = data.get('name')
    data_path = f'{RESULTS_DIR}/{name}.json'
    json.dump(data, open(data_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)


# 通过for循环，依次实现10个页面的爬取
# def main():
#     start_time = time.time()
#     for i in range(1, 11):
#         index_html = scrape_index(i)  # 得到一个页面的html
#         partUrlList = parse_index(index_html)  # 得到该页面中所有详情页的url片段
#         for partUrl in partUrlList:
#             detail_html = scrape_detail(partUrl)  # 构造完整的详情页url，并爬取详情页
#             print(parse_detail(detail_html))
#             data = parse_detail(detail_html)  # 解析获得详情页的数据
#             save_data(data)
#     end_time = time.time()
#     print("总用时：", end_time - start_time)
#
# main()


# 使用多进程实现10个页面同时爬取
def main(pageNum):
    index_html = scrape_index(pageNum)
    partUrlList = parse_index(index_html)
    for partUrl in partUrlList:
        detail_html = scrape_detail(partUrl)
        print(parse_detail(detail_html))
        data = parse_detail(detail_html)
        logging.info('得到详细信息：%s', data)
        logging.info('保存为json文件')
        save_data(data)
        logging.info('文件被成功保存')


if __name__ == '__main__':
    pool = multiprocessing.Pool()
    pages = range(1, TOTAL_PAGE + 1)
    start_time = time.time()
    pool.map(main, pages)
    pool.close()
    pool.join()
    end_time = time.time()
    print("总用时：", end_time - start_time)
