import os
import argparse
from spider import Spider
from datahelper import DataHelper

output_keywords = [["title", "标题"], ["keywords", "关键词"], ["time", "日期"], ["section", "分类"], ["content", "内容"], ["url", "网址"]]

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--more_news_times", type=int, default=1, help="Number of click the 'more news' button")
    parser.add_argument("--threading_num", type=int, default=3, help="Number of threading")
    parser.add_argument('-o', "--output_dir", type=str, default="../output")
    parser.add_argument('-i', "--ip_list_file", type=str, default="../input/alive_ip_list.txt")
    parser.add_argument('-v', "--visited_url", type=str, default="../input/visited_url.txt")
    parser.add_argument('-u', "--unvisited_url", type=str, default="../input/unvisited_url.txt")
    parser.add_argument('-r', "--root_url", type=str, default="../input/root_url.txt")
    args = parser.parse_args()

    datahelper = DataHelper()
    spider = Spider(datahelper=datahelper, args=args)
    spider.start()