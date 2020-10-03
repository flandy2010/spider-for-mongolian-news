from page_scrapy import get_page, get_url
from datahelper import DataHelper

class Spider():

    def __init__(self, datahelper, args):
        self.datahelper = datahelper
        self.args = args

    def start(self):
        visited_url_set = set(self.datahelper.read_list(self.args.visited_url))
        root_url = self.datahelper.read_list(self.args.root_url)

        # 获取更新的新闻url地址，并去重
        new_url_set = self.get_url(root_url[:3])
        unvisited_url_list = []
        for url in list(new_url_set):
            if url in visited_url_set:
                continue
            unvisited_url_list.append(url)

        # 爬取新的页面

        # 输出

    def get_url(self, root_list):
        url_set = get_url(root_list, more_news_time=self.args.more_news_times)
        return url_set

    def get_page(self, url_list):
        pass

    def get_visited_url_set(self):
        pass

    def write_visited_url_set(self):
        pass


if __name__=="__main__":
    datahelper = DataHelper()
    spider = Spider(datahelper=datahelper, args=None)