import requests
from bs4 import BeautifulSoup
from utils import content_abstact

def get_page(page_url):
    # 伪装工作
    r = requests.get(url=page_url)
    if r.status_code != 200:
        print("爬取失败，state code: %d" % (r.status_code))
        return None
    # print(r.text)

    # 数据处理工作
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

    return result

if __name__=="__main__":
    test_url = "https://gogo.mn/r/y6vg2"
    get_page(test_url)