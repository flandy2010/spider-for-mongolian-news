import re

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