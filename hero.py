import json
import time

import log_util
import ui_util
from load_config import get_coordinate_info


class HeroManager:
    def __init__(self):
        self.hero_map = {}
        self.log = log_util.Logger()
        self.hero_info = {}
        self.is_success = False
        self.coordinate_info = get_coordinate_info()
        self.fighting_info = self.coordinate_info["战斗界面"]
        map_data = self.fighting_info["英雄检查点"]
        y = map_data["y"]
        self.check_points = [
            (map_data["x1"], y),
            (map_data["x2"], y),
            (map_data["x3"], y),
            (map_data["x4"], y),
        ]

    def load_hero_map(self):
        try:
            with open("hero.json", 'r', encoding='utf-8') as file:
                data = json.load(file)
            for level, heroes in data.items():
                for name, obj in heroes.items():
                    if "valid_checking_list" in obj and obj["valid_checking_list"]:
                        for valid_checking in obj["valid_checking_list"]:
                            key = "".join(valid_checking)
                            self.hero_map[key] = obj
        except FileNotFoundError:
            self.log.error("英雄数据文件 hero.json 未找到")
        except json.JSONDecodeError:
            self.log.error("加载英雄数据时发生 JSON 解析错误")

    def get_current_hero_color_info(self):
        return [
            ui_util.get_color_at_coordinate(x, y) for x, y in self.check_points
        ]

    def update_current_hero_info(self):
        self.hero_info = {}
        # 加载必要数据
        if not self.coordinate_info:
            self.load_coordinate_info()
        if not self.hero_map:
            self.load_hero_map()

        # 定义 X 和 Y 范围
        x_range = range(1, 4)
        y_range = range(1, 7)
        xy_array = [f"{x}-{y}" for y in y_range for x in x_range]

        # 提取格子地图
        grid_map = self.coordinate_info.get("战斗界面", {}).get("格子", {})

        # 遍历所有坐标
        for grid in xy_array:
            # 跳过不存在的格子
            if grid not in grid_map:
                self.log.debug(f"坐标 {grid} 不存在于地图中，跳过")
                continue

            # 获取格子坐标
            x, y = grid_map[grid]["x"], grid_map[grid]["y"]

            # 执行点击操作
            ui_util.click(x, y)

            try:
                # 获取验证点的颜色
                color = ui_util.get_color_at_coordinate(*(
                    [self.fighting_info["英雄检查点"]["valid_check_x"],
                     self.fighting_info["英雄检查点"]["valid_check_y"]]))

                # 校验颜色是否匹配
                if self.fighting_info["英雄检查点"]["valid_check_color"] == color:
                    # 获取当前英雄的颜色信息作为键值
                    key = "".join(self.get_current_hero_color_info())

                    # 检查 key 是否在 hero_map 中
                    if key in self.hero_map:
                        inner_hero = self.hero_map[key]
                        name = inner_hero["name"]
                        self.hero_info[grid] = inner_hero["id"]
                        self.log.debug(f"匹配到英雄: {name}，坐标: {grid}, x: {x}, y: {y}")
                    else:
                        self.log.debug(f"英雄数据未匹配: 当前 key {key}")
                else:
                    self.log.debug(f"颜色校验失败: 坐标 {grid}, 当前颜色: {color}")
            except KeyError as e:
                # 捕获 KeyError 并记录日志
                self.log.warn(f"英雄数据未匹配: {str(e)}, 当前坐标 {grid}")
            except Exception as e:
                # 捕获其他异常
                self.log.error(f"未知错误: {str(e)}, 坐标 {grid}")
        return dict

    def deal_with_hero(self):
        save_list = [15, 12, 1, 2, 3]
        # 定义 X 和 Y 范围
        x_range = range(1, 4)
        y_range = range(1, 7)
        xy_array = [f"{x}-{y}" for y in y_range for x in x_range]

        # 提取格子地图
        grid_map = self.coordinate_info.get("战斗界面", {}).get("格子", {})

        try:

            # 遍历所有坐标
            for grid in xy_array:
                # 跳过不存在的格子
                if grid not in grid_map or grid not in self.hero_info:
                    self.log.debug(f"坐标 {grid} 不存在于地图中或无英雄，跳过")
                    continue
                current_hero = self.hero_info[grid]
                if current_hero not in save_list and current_hero < 20:
                    self.do_sell(grid_map[grid]["x"], grid_map[grid]["y"])
                elif current_hero == 1:
                    if grid != "3-1" and self.hero_info["3-1"] != 1:
                        ui_util.move_to(grid_map[grid]["x"], grid_map[grid]["y"],
                                        grid_map["3-1"]["x"], grid_map["3-1"]["y"])
                    elif grid != "3-1":
                        self.do_sell(grid_map[grid]["x"], grid_map[grid]["y"])
                elif current_hero == 33:
                    ui_util.click(grid_map[grid]["x"], grid_map[grid]["y"])
                    ui_util.click(
                        grid_map[grid]["x"] + self.fighting_info["合成偏移"]["x"],
                        grid_map[grid]["y"] + self.fighting_info["合成偏移"]["y"])
                elif current_hero == 37:
                    if grid != "1-1" and self.hero_info["1-1"] != 37:
                        ui_util.move_to(grid_map[grid]["x"], grid_map[grid]["y"],
                                        grid_map["1-1"]["x"], grid_map["1-1"]["y"])
        except KeyError as e:
            return

    def do_sell(self, x, y):
        ui_util.click(x, y)
        for i in range(3):
            ui_util.click(x + self.fighting_info["出售偏移"]["x"], y + self.fighting_info["出售偏移"]["y"])

    def call_if_necessary(self):
        self.log.debug("尝试召唤英雄")
        values = self.hero_info.values()
        if 1 in values and 2 in values and 3 in values and (
                list(self.hero_info.values()).count(1) + list(self.hero_info.values()).count(2) + list(
                self.hero_info.values()).count(3) >= 5):
            return False

        self.back_to_fighting_main()
        for i in range(5):
            ui_util.click(self.fighting_info["召唤"]["x"], self.fighting_info["召唤"]["y"])
        self.back_to_fighting_main()
        return True

    def back_to_fighting_main(self):
        self.log.debug("尝试返回主战斗界面")
        ui_util.click(self.fighting_info["强化"]["取消"]["x"],
                      self.fighting_info["强化"]["取消"]["y"])

    def call_boss(self):
        self.log.debug("尝试召唤boss")
        ui_util.click(self.fighting_info["BOSS挑战"]["x"],
                      self.fighting_info["BOSS挑战"]["y"])

    def pray_if_necessary(self):
        self.log.debug("尝试祈愿英雄")
        values = self.hero_info.values()
        if 12 in values and 15 in values and (
                list(self.hero_info.values()).count(12) + list(self.hero_info.values()).count(15) >= 3):
            return False
        self.back_to_fighting_main()
        pray = self.fighting_info["祈愿"]
        ui_util.click(pray["x"], pray["y"])
        for i in range(7):
            ui_util.click(pray["稀有"]["x"], pray["稀有"]["y"])
            time.sleep(0.7)
        self.back_to_fighting_main()
        return True

    def quit_if_finished(self):
        res = False
        color = ui_util.get_color_at_coordinate(self.fighting_info["结束战斗"]["确认"]["x"],
                                                self.fighting_info["结束战斗"]["确认"]["y"])
        if color == self.fighting_info["结束战斗"]["确认"]["color"]:
            label_color = ui_util.get_color_at_coordinate(self.fighting_info["结束战斗"]["标记"]["x"],
                                                          self.fighting_info["结束战斗"]["标记"]["y"])
            if label_color == self.fighting_info["结束战斗"]["标记"]["胜利"]:
                self.log.info("结束战斗，胜利")
                res = True
                self.is_success = True
            else:
                self.log.info("结束战斗，失败")
            ui_util.click(self.fighting_info["结束战斗"]["确认"]["x"],
                          self.fighting_info["结束战斗"]["确认"]["y"])
        return res

    def need_call_or_pray(self):
        '''
        根据天使的数量是否大于2判断是否需要召唤或祈愿
        :return:
        '''

        return not list(self.hero_info.values()).count(37) >= 1

    def call_superstar(self):
        ui_util.click(self.fighting_info["神话召唤"]["2"]["x"], self.fighting_info["神话召唤"]["2"]["y"])

    def cycling_fighting(self):
        self.wait_for_80()
        while True:
            self.adjust_speed()
            if manager.need_call_or_pray():
                manager.update_current_hero_info()
                call1 = manager.call_if_necessary()
                call2 = manager.pray_if_necessary()
                if not call1 and not call2:
                    manager.call_superstar()
                manager.deal_with_hero()

            else:
                self.upgrade_superstar_level()
            manager.call_boss()

            if manager.quit_if_finished():
                return self.is_success
            time.sleep(5)

    def adjust_speed(self):
        color = ui_util.get_color_at_coordinate(self.fighting_info["速度"]["x"], self.fighting_info["速度"]["y"], )
        if color == self.fighting_info["速度"]["color"]:
            ui_util.click_target(self.fighting_info["速度"]["x"], self.fighting_info["速度"]["y"])

    def upgrade_superstar_level(self):
        self.back_to_fighting_main()
        ui_util.click(self.fighting_info["强化"]["x"], self.fighting_info["强化"]["y"])
        for i in range(5):
            ui_util.click(self.fighting_info["强化"]["神话、传说英雄强化"]["x"],
                          self.fighting_info["强化"]["稀有英雄强化"]["y"])
        self.back_to_fighting_main()

    def wait_for_80(self):
        time.sleep(5)
        start_time = time.time()
        color = ui_util.get_color_at_coordinate(self.fighting_info["80"]["x"], self.fighting_info["80"]["y"])
        target_color = self.fighting_info["80"]["color"]
        while color == target_color:
            color = ui_util.get_color_at_coordinate(self.fighting_info["80"]["x"], self.fighting_info["80"]["y"])
            if time.time() - start_time > 3000:
                break
        self.call_if_necessary()
        self.log.debug("到80了")


if __name__ == '__main__':
    manager = HeroManager()
    manager.cycling_fighting()

#
# if __name__ == '__main__':
#     manager = HeroManager()
#     manager.quit_if_finished()
