import os
from page_scrapy import get_page
from datahelper import DataHelper

output_keywords = [["title", "标题"], ["keywords", "关键词"], ["time", "日期"], ["section", "分类"], ["content", "内容"], ["url", "网址"]]

if __name__=="__main__":
    datahelper = DataHelper()
    data = get_page("https://gogo.mn/r/y6vg2")
    datahelper.output_dict(data, "./output/test.txt", output_keywords)