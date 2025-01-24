import json
import time

import pyautogui

import ui_util
import window_util


class InitResolution:

    def __init__(self):
        self.data = None
        self.offset_x = window_util.get_window_offset_x()
        self.offset_y = window_util.get_window_offset_y()

    def deal_grid_quick(self, node):
        print("当前正在获取计算防卫台坐标，请点击自身炮台的左上角")
        current_x, current_y = pyautogui.position()
        left_up_x = current_x - self.offset_x
        left_up_y = current_y - self.offset_y
        print(left_up_x, left_up_y)

        print("当前正在获取计算防卫台坐标，请点击自身炮台的右上角")
        current_x, current_y = pyautogui.position()
        right_up_x = current_x - self.offset_x
        right_up_y = current_y - self.offset_y
        print(right_up_x, right_up_y)

        print("当前正在获取计算防卫台坐标，请点击自身炮台的左下角")
        current_x, current_y = pyautogui.position()
        left_down_x = current_x - self.offset_x
        left_down_y = current_y - self.offset_y
        print(left_down_x, left_down_y)

        print("当前正在获取计算防卫台坐标，请点击自身炮台的右下角")
        current_x, current_y = pyautogui.position()
        right_down_x = current_x - self.offset_x
        right_down_y = current_y - self.offset_y
        print(right_down_x, right_down_y)

        left = (left_up_x + left_down_x) / 2
        right = (right_up_x + right_down_x) / 2
        up = (left_up_y + right_up_y) / 2
        down = (right_down_y + left_down_y) / 2

        width = right - left
        height = down - up
        print("防卫台坐标已定位完成,现在以1-1，2-1，3-1，1-2...的顺序会模拟点击每个点位")

        width_per_grid = width / 6
        height_per_grid = height / 3
        for x in range(1, 7):
            for y in range(1, 4):
                key = str(y) + "-" + str(x)
                node[key]["x"] = left + (x - 0.5) * width_per_grid
                node[key]["y"] = up + (y - 0.5) * height_per_grid
                ui_util.click_target(node[key]["x"], node[key]["y"])
                time.sleep(0.5)

        print("模拟点击完成，确认每个点位无误后继续")

    def deal_valid_check_point(self, node, path):
        print("当前正在获取计算英雄检查点，请选择任意英雄后点击英雄框的左侧突出点")
        current_x, current_y = pyautogui.position()
        left_x = current_x - self.offset_x
        left_y = current_y - self.offset_y
        print(left_x, left_y)

        print("当前正在获取计算英雄检查点，请选择任意英雄后点击英雄框的右侧突出点")
        current_x, current_y = pyautogui.position()
        right_x = current_x - self.offset_x
        right_y = current_y - self.offset_y
        print(right_x, right_y)

        width = right_x - left_x
        height = right_y - left_y
        width_per_grid = width / 3
        height_per_grid = height / 3
        print("英雄检查点已定位完成,现在以会模拟点击每个点位")
        for x in range(4):
            node[str(x + 1)]["x"] = left_x + x * width_per_grid
            node[str(x + 1)]["y"] = left_y + x * height_per_grid
            ui_util.click_target(node[str(x + 1)]["x"], node[str(x + 1)]["y"])
            time.sleep(0.5)

        self.traverse_and_process(node["合法性检测"], path + "-" + "合法性检测")

    def process_json_file(self, file_name):
        start = time.time()
        parent_dir = "resolution/"
        source_file = parent_dir + "source.json"
        target_file = parent_dir + file_name

        # 读取 JSON 文件
        with open(source_file, 'r', encoding='utf-8') as file:
            self.data = json.load(file)

        # 开始处理 JSON 数据
        self.traverse_and_process(self.data, "根")

        spend = time.time() - start
        if spend < 100:
            print("请使用调试模式进行点击取点，本次结果不保存")
            print(self.data)
            return

            # 保存修改后的数据到原文件
        with open(target_file, 'w', encoding='utf-8') as file:
            json.dump(self.data, file, indent=4, ensure_ascii=False)

        print("分辨率采集结束，本次采集共花费", spend + "秒，数据已保存到" + target_file)

    def traverse_and_process(self, node, path):
        if not isinstance(node, dict):
            return
            # 如果当前字典包含 x 和 y，模拟鼠标点击并记录坐标
        if path.endswith("格子"):
            self.deal_grid_quick(node)
            return
        elif path.endswith("英雄检查点"):
            self.deal_valid_check_point(node, path)
            return
        elif 'x偏移' in node and 'y偏移' in node:
            self.deal_offset_quick(node, path)
            return
        elif 'x' in node and 'y' in node:
            print_str = path
            if 'color' in node:
                print_str = print_str + "|该点需要采集彩色信息"
            if "tip" in node:
                print("!!!注意" + node['tip'])
            print(print_str)
            # 获取当前鼠标位置
            current_x, current_y = pyautogui.position()
            node['x'] = current_x - self.offset_x
            node['y'] = current_y - self.offset_y
            print(current_x, current_y, node['x'], node['y'])

            # 如果包含 color，记录当前位置颜色
            if 'color' in node:
                # 通过屏幕截图获取颜色（示例方法）
                screenshot = pyautogui.screenshot()
                pixel_color = screenshot.getpixel((current_x, current_y))
                color = f'#{pixel_color[0]:02x}{pixel_color[1]:02x}{pixel_color[2]:02x}'
                print(color)
                node['color'] = color

        # 如果当前节点是字典，递归遍历
        if isinstance(node, dict):
            for key, value in node.items():
                if key == "x" or key == "y" or key == "color":
                    continue

                # 递归遍历嵌套的子节点
                self.traverse_and_process(value, path + "-" + key)

        # 如果当前节点是列表，递归遍历每个元素
        elif isinstance(node, list):
            for item in node:
                self.traverse_and_process(item, path + "-" + node)

    def deal_offset_quick(self, node, path):
        print("正在准备获取" + path + "，请保证在3-3的英雄可以进行该操作")
        origin_x = self.data["战斗界面"]["格子"]["3-3"]["x"]
        origin_y = self.data["战斗界面"]["格子"]["3-3"]["y"]

        current_x, current_y = pyautogui.position()
        node["x偏移"] = current_x - origin_x - self.offset_x
        node["y偏移"] = current_y - origin_y - self.offset_y
        print(node["x偏移"], node["y偏移"])


if __name__ == '__main__':
    i = InitResolution()
    i.process_json_file("macmini.json")
