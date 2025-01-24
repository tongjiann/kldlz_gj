import datetime
import time

import log_util
import ui_util
from hero import HeroManager
from load_config import get_coordinate_info

main_info = {}

total_time = 0

success_time = 0

log = log_util.get_logger()


def buy_energy():
    log.info("开始买体力")
    main_info = get_coordinate_info()["主界面"]
    energy_info = main_info["联合作战"]["精力"]
    ui_util.click_target(energy_info["x"], energy_info["y"])
    free_x = energy_info["免费精力"]["x"]
    free_y = energy_info["免费精力"]["y"]
    free_color = ui_util.get_color_at_coordinate(free_x, free_y)
    if free_color == energy_info["免费精力"]["color"]:
        for i in range(5):
            ui_util.click_slow(free_x, free_y)
            ui_util.click_slow(main_info["联合作战"]["x"], main_info["联合作战"]["y"])
        ui_util.click_slow(main_info["联合作战"]["x"], main_info["联合作战"]["y"])
        log.info("购买免费精力")
        return True
    today_x = energy_info["今天"]["x"]
    today_y = energy_info["今天"]["y"]
    today_color = ui_util.get_color_at_coordinate(today_x, today_y)
    if today_color == energy_info["今天"]["color"]:
        ui_util.click_slow(today_x, today_y)
        ui_util.click_slow(main_info["联合作战"]["x"], main_info["联合作战"]["y"])
        ui_util.click_slow(main_info["联合作战"]["x"], main_info["联合作战"]["y"])
        log.info("购买今日精力")
        return True
    miss_x = energy_info["错过"]["x"]
    miss_y = energy_info["错过"]["y"]
    miss_color = ui_util.get_color_at_coordinate(miss_x, miss_y)
    print(miss_color)
    if miss_color == energy_info["错过"]["color"]:
        ui_util.click_slow(miss_x, miss_y)
        ui_util.click_slow(energy_info["错过"]["x1"], energy_info["错过"]["y1"])
        ui_util.click_slow(main_info["联合作战"]["x"], main_info["联合作战"]["y"])
        ui_util.click_slow(main_info["联合作战"]["x"], main_info["联合作战"]["y"])
        ui_util.click_slow(main_info["联合作战"]["x"], main_info["联合作战"]["y"])
        log.info("购买错过精力")
        return True
    return False


if __name__ == '__main__':
    global coordinate_info
    # 加载坐标信息
    main_info = get_coordinate_info()["主界面"]
    manager = HeroManager()
    ui_util.click_slow(main_info["联合作战"]["x"], main_info["联合作战"]["y"])
    while True:
        time.sleep(1)
        random_x = main_info["联合作战"]["随机匹配"]["x"]
        random_y = main_info["联合作战"]["随机匹配"]["y"]
        log.info("准备进入联合作战")
        ui_util.click_slow(random_x, random_y)
        time.sleep(5)
        color = ui_util.get_color_at_coordinate(random_x, random_y)
        if color == main_info["联合作战"]["随机匹配"]["color"]:
            log.info("没有精力了，要去买体力")
            buy_energy()
        else:
            manager.cycling_fighting()
