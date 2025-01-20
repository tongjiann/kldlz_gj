import configparser
import json


def get_coordinate_info():
    # 创建一个配置解析器
    config = configparser.ConfigParser()

    # 读取现有配置文件
    config.read('config.ini')
    coordinate_file = config.get('file', 'coordinate_file')

    # 从文件读取 JSON
    with open(coordinate_file, 'r', encoding='utf-8') as file:
        return json.load(file)
