## 项目介绍
本项目用于爬取蒙古国新闻网站:[gogo新闻网](www.gogo.mn)每日更新的新闻。

## 环境依赖
- 1、pip install -r requirements
- 2、selenuim库需要下载浏览器以及对应的driver，详情参考：[selenuim-安装各浏览器的驱动](https://www.cnblogs.com/ssj0723/p/9128731.html)

## 参数说明
- --more\_news\_times 设置需要点击多少次“更多新闻”按钮
- --threading_num 同时爬取的线程数
- -o --output_dir 输出文件夹路径
- -i --ip_list_file 存放可用ip的文件路径
- -v --visited_url 存放访问过的url的文件路径
- -u --unvisited_url 存放尚未访问的url的文件路径
- -r --root_url 存放用于提取新闻url的根网址文件

## 运行

`python main.py -o output_dir -r root_url_file -v visited_url_file`