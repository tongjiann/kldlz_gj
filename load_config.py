import configparser
import json


def get_coordinate_info():
    coordinate_file = get_env()

    # 从文件读取 JSON
    with open("resolution/" + coordinate_file, 'r', encoding='utf-8') as file:
        return json.load(file)


def get_env():
    # 创建一个配置解析器
    config = configparser.ConfigParser()
    # 读取现有配置文件
    config.read('config.ini')
    return config.get('file', 'coordinate_file')


def get_hero_info():
    # 创建一个配置解析器
    config = configparser.ConfigParser()

    # 读取现有配置文件
    config.read('config.ini')
    coordinate_file = config.get('file', 'coordinate_file')

    # 从文件读取 JSON
    with open("hero/" + coordinate_file, 'r', encoding='utf-8') as file:
        return json.load(file)
