import re
import time
import random
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from utils import content_abstact, get_agent_pc


def get_page(page_url, headers=None, proxy=None):
    # 伪装工作
    if not headers:
        headers = {
            "User-Agent": get_agent_pc(),
            'Referer': "https://gogo.mn"
        }

    r = requests.get(url=page_url, headers=headers, proxies=proxy)
    if r.status_code != 200:
        print("爬取失败，state code: %d" % (r.status_code))
        return None

    # 数据处理工作
    try:
        soup = BeautifulSoup(r.text, "html.parser")

        result = {"title": None, "section": None, "time": None, "author": None, "keywords": None, "description":None, "content": None, "url": page_url}
        result["title"] = soup.title.contents[0].strip()

        for data in soup.find_all("meta"):
            if not "name" in data.attrs:
                continue
            result["section"] = data.attrs["content"].strip() if data.attrs["name"]=="section" else result["section"]
            result["time"] = data.attrs["content"].strip() if data.attrs["name"]=="last-modified" else result["time"]
            result["keywords"] = data.attrs["content"].strip().split(",") if data.attrs["name"]=="keywords" else result["keywords"]
            result["description"] = data.attrs["content"].strip() if data.attrs["name"]=="description" else result["description"]

        result["content"] = content_abstact(soup)
    except:
        result = None

    return result


def get_url(root_url, more_news_time=10):
    """
    根据一些根网址，获取新闻页面的url。考虑到根网页通常使用点击按钮后加载的方式，因此采用了selenium库
    :param root_url: 根网址列表
    :param more_news_time: 点击多少次“更多新闻”按钮来展开网页
    :return:
    """
    url_set = set()

    driver = webdriver.Firefox()
    driver.get(root_url)
    print(">>> Successfully visit root url: %s" % root_url)

    # 展开网页
    for x in range(more_news_time):
        print("Click 'More news' button (%d times)" % (x + 1))
        # 待修改
        driver.find_element_by_xpath("/html/body/div[2]/div[2]/section[1]/div/div/div[1]/div[2]/div[1]/div/div[1]/a/div").click()
        time.sleep(2 + 4 * random.random())

    # 获取网页内部的url
    soup = BeautifulSoup(driver.page_source, "html.parser")
    pattern = re.compile(r'/r/[0-9a-z]{5}')
    for tag in soup.find_all("a"):
        if "href" not in tag.attrs:
            continue
        res = re.match(pattern, tag.attrs["href"])
        if res:
            url = "https://gogo.mn%s" % res.group()
            url_set.add(url)

    driver.quit()

    return url_set


if __name__=="__main__":
    original_url = "http://httpbin.org/get"
    test_url = "https://gogo.mn/r/y6vg2"
    test_root_list = ["https://gogo.mn/i/2"]

    # get_page(original_url)
    get_url(test_root_list, more_news_time=2)
