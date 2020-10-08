import os

class DataHelper():

    def __init__(self):
        pass

    def read_list(self, file_path):
        """
        读入本地的list文件
        :param file_path:输入的文件路径
        :return:
        """
        if not os.path.exists(file_path):
            print("File not exists ! [%s]" % file_path)
            return []

        data = []
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f.readlines():
                if line.strip() != "":
                    data.append(line.strip())
        return data

    def write_list(self, data, file_path):
        """
        将list数据写入本地
        :param data: list类型的数据
        :param file_path: 输出的文件路径
        :return:
        """
        if os.path.exists(file_path):
            os.remove(file_path)
        with open(file_path, "a", encoding="utf-8") as f:
            for value in data:
                f.write("%s\n" % (str(value).strip()))
        return

    def write_dict(self, file_path, data, keyword_list=None):
        """
        将dict数据输出到本地
        :param data: dict数据
        :param file_path: 输出的文件路径
        :param keyword_list: list[[str, str],...] 用来表示需要优先输出的关键词。
        :return:
        """

        def list_to_str(data):
            if type(data)==list:
                return ",".join(data)
            else:
                return data

        if os.path.exists(file_path):
            os.remove(file_path)

        with open(file_path, "a", encoding="utf-8") as f:
            for keyword, output_key in keyword_list:
                if keyword in data:
                    f.write("【%s】: %s\n" % (output_key, list_to_str(data[keyword])))

            keywords = [data[0] for data in keyword_list]
            for k, v in data.items():
                if k in keywords:
                    continue
                f.write("【%s】: %s\n" % (k, list_to_str(v)))

        return
