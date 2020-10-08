import re
import os
import random
import requests
import threading
from bs4 import BeautifulSoup

def text_abstract(data):
    """
    提取网页中的内容。提取方法为，用非贪婪的方法删去“<.*?>”的内容，保留剩下的
    :param data: 网页数据
    :return: str
    """
    pattern = re.compile(r'<.*?>')
    data = re.sub(pattern, "", data).strip()
    return data


def content_abstact(soup):
    data_list = soup.find_all(class_="not-short-read uk-container uk-column-1-1 uk-column-divider seo-bagana")
    content = ""
    for child in data_list[0].children:
        content = content + text_abstract(str(child).strip()) + "\n"

    return content.strip()


def get_agent_pc():
    user_agent_pc = [
        # 谷歌
        'Mozilla/5.0.html (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.html.2171.71 Safari/537.36',
        'Mozilla/5.0.html (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.html.1271.64 Safari/537.11',
        'Mozilla/5.0.html (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.html.648.133 Safari/534.16',
        # 火狐
        'Mozilla/5.0.html (Windows NT 6.1; WOW64; rv:34.0.html) Gecko/20100101 Firefox/34.0.html',
        'Mozilla/5.0.html (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10',
        # opera
        'Mozilla/5.0.html (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.html.2171.95 Safari/537.36 OPR/26.0.html.1656.60',
        # qq浏览器
        'Mozilla/5.0.html (compatible; MSIE 9.0.html; Windows NT 6.1; WOW64; Trident/5.0.html; SLCC2; .NET CLR 2.0.html.50727; .NET CLR 3.5.30729; .NET CLR 3.0.html.30729; Media Center PC 6.0.html; .NET4.0C; .NET4.0E; QQBrowser/7.0.html.3698.400)',
        # 搜狗浏览器
        'Mozilla/5.0.html (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.html.963.84 Safari/535.11 SE 2.X MetaSr 1.0.html',
        # 360浏览器
        'Mozilla/5.0.html (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.html.1599.101 Safari/537.36',
        'Mozilla/5.0.html (Windows NT 6.1; WOW64; Trident/7.0.html; rv:11.0.html) like Gecko',
        # uc浏览器
        'Mozilla/5.0.html (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.html.2125.122 UBrowser/4.0.html.3214.0.html Safari/537.36',
    ]
    return random.choice(user_agent_pc)


def build_ip_pool(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
    ip_list = []

    url = "http://www.xiladaili.com/"
    pattern = re.compile(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}')
    r = requests.get(url, headers={"User-Agent": get_agent_pc()})
    soup = BeautifulSoup(r.text, "html.parser")

    for table in soup.find_all("tr"):
        for data in table.find_all("td"):
            if data.contents is None:
                break
            r = re.match(pattern, data.contents[0])
            if r:
                ip = str(r.group())
                ip_list.append(ip)

    ip_list = ip_list
    label_list = [False for _ in range(len(ip_list))]
    print(len(label_list))

    def test_ip_alive(p, ip_list, label_list, thread_num):
        while p < len(ip_list):
            try:
                ip = ip_list[p]
                # print("Thread: %s, p = %d, alive=%d\n" % (threading.current_thread().name, p, threading.activeCount()))
                proxy = {'http': ip, 'https': ip}
                response = requests.get('https://httpbin.org/ip', proxies=proxy, timeout=3)
                print("使用ip:%s, 伪装成功" % ip)
                mutex.acquire()
                label_list[p] = True
                mutex.release()
            except:
                # print("使用ip:%s, 伪装失败" % ip)
                pass
            p += thread_num
        return

    thread_num = 8
    thread_list = []
    mutex = threading.Lock()

    for x in range(thread_num):
        thread = threading.Thread(target=test_ip_alive, args=(x, ip_list, label_list, thread_num, ), name='Thread-%d' % x)
        thread.start()
        thread_list.append(thread)

    for thread in thread_list:
        thread.join()

    with open(file_path, "a", encoding="utf-8") as f:
        for x in range(len(ip_list)):
            if label_list[x]:
                f.write("%s\n" % ip_list[x])




if __name__=="__main__":

    build_ip_pool("../output/alive_ip_list.txt")