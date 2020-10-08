import os
import time
import random
import threading
from page_scrapy import get_page, get_url
from utils import build_ip_pool, get_agent_pc
from datahelper import DataHelper

class Spider():

    def __init__(self, datahelper, args):
        self.datahelper = datahelper
        self.args = args
        self.visited_url_set = self.get_visited_url_set()
        self.unvisited_url_list = self.get_unvisited_url_list()
        self.root_url_list = self.get_root_url()

        # build_ip_pool(self.args.ip_list_file)
        self.ip_dict = self.get_ip_dict()

    def start(self):
        # 获取更新的新闻url地址，并去重
        # self.download_url()

        # 多线程爬取新的页面
        thread_list = []
        thread_num = self.args.threading_num

        for x in range(thread_num):
            thread = threading.Thread(target=self.download_page, args=(x, thread_num, ), name='Thread-%d' % x)
            print(">>> Thread-%d start" % x)
            thread.start()
            thread_list.append(thread)

        for thread in thread_list:
            thread.join()

        # 更新没有爬取的列表
        new_unvisited_url_list = []
        for url in self.unvisited_url_list:
            if url not in self.visited_url_set:
                new_unvisited_url_list.append(url)
        self.unvisited_url_list = new_unvisited_url_list

        # 输出列表信息
        self.write_unvisited_url_list()
        self.write_visited_url_set()

    def download_url(self):
        for root_url in self.root_url_list[11:]:
            url_set = get_url(root_url, more_news_time=self.args.more_news_times)
            num = 0
            for url in url_set:
                if url in self.visited_url_set or url in self.unvisited_url_list:
                    continue
                num += 1
                self.unvisited_url_list.append(url)
                with open(self.args.unvisited_url, "a", encoding="utf-8") as f:
                    f.write("%s\n" % url)
                time.sleep(5 + random.random() * 3)
            print(">>> INFO: Found %d new urls from page %s" % (num, root_url))
        return

    def download_page(self, p, thread_num):
        while p < len(self.unvisited_url_list):

            url = self.unvisited_url_list[p]
            try_num = 0

            while True:
                try:
                    ip, proxy = self.get_proxy()
                    proxy = None                                # 发现反爬机制较弱，没有使用ip池。
                    headers = {
                        "User-Agent": get_agent_pc(),
                        'Referer': "https://gogo.mn"
                    }
                    data = get_page(url, headers=headers, proxy=proxy)
                    if data is None:
                        try_num += 1
                        self.ip_dict[ip] += 1
                        if self.ip_dict[ip] > 3:
                            self.ip_dict.pop(ip)
                        if try_num >= 3:
                            break
                        time.sleep(random.random() * 5 + try_num * 5)
                        continue
                    else:
                        title_data = data["title"].replace(".", "·")
                        for char in [":", "<", ">", "|", "/", "？", "?", "*", "\""]:
                            title_data = title_data.replace(char, "")
                        time_data = data["time"].split("T")[0]
                        file_name = "%s - %s.txt" % (time_data, title_data)
                        file_path = os.path.join(self.args.output_dir, file_name)
                        self.output_page(file_path, data)
                        self.visited_url_set.add(url)
                        print("Thread：%s get No.%d page：%s successfully" % (threading.current_thread().name, p, url))
                        time.sleep(random.random() * 5 + 5)
                        break
                except Exception as e:
                    print("%s, retrying" % e)
                    try_num += 1
                    if try_num >= 3:
                        break
                    continue

            p += thread_num

    def output_page(self, file_path, page_data):
        output_keywords = [["title", "标题"], ["keywords", "关键词"], ["time", "日期"], ["section", "分类"], ["content", "内容"],
                           ["url", "网址"]]
        self.datahelper.write_dict(file_path, page_data, output_keywords)

    def get_root_url(self):
        data = self.datahelper.read_list(self.args.root_url)
        print(">>> Read %d root url list successfully !" % len(data))
        return data

    def get_visited_url_set(self):
        data = set(self.datahelper.read_list(self.args.visited_url))
        print(">>> Read visited url list successfully !")
        return data

    def get_unvisited_url_list(self):
        data = self.datahelper.read_list(self.args.unvisited_url)
        print(">>> Read un-visited %d urls list successfully ! " % len(data))
        return data

    def get_ip_dict(self):
        alive_ip_list = self.datahelper.read_list(self.args.ip_list_file)
        ip_dict = {}
        for ip in alive_ip_list:
            ip_dict[ip] = 0
        print(">>> Read %d alive ip list successfully !" % len(ip_dict))
        return ip_dict

    def write_unvisited_url_list(self):
        self.datahelper.write_list(self.unvisited_url_list, self.args.unvisited_url)

    def write_visited_url_set(self):
        self.datahelper.write_list(list(self.visited_url_set), self.args.visited_url)

    def get_proxy(self):
        if len(self.ip_dict.keys())==0:
            return "", None
        ip = random.choice(list(self.ip_dict.keys()))
        proxy = {'http': ip, 'https': ip}
        return ip, proxy