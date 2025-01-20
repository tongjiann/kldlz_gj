import configparser
import json

coordinate_info = {}


def load_coordinate_info():
    global coordinate_info
    # 创建一个配置解析器
    config = configparser.ConfigParser()

    # 读取现有配置文件
    config.read('config.ini')
    coordinate_file = config.get('file', 'coordinate_file')

    # 从文件读取 JSON
    with open(coordinate_file, 'r', encoding='utf-8') as file:
        coordinate_info = json.load(file)


def start_fighting():
    coordinate_info[""]


def update_hero_info():
    pass


def do_fighting():
    # 更新当前每格状态
    update_hero_info()
    # 进行召唤

    # 进行祈愿

    # 进行神话召唤

    pass


if __name__ == '__main__':
    # 加载坐标信息
    load_coordinate_info()

    # 开始联合作战
    start_fighting()

    进行联合作战
    do_fighting()
