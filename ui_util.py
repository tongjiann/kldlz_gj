import random
import pyautogui
from PIL import ImageGrab
import window_util

offset_x = 0
offset_y = 0

is_load = False
need_random_offset = True


def do_load():
    global offset_x
    global offset_y
    global is_load
    offset_x = window_util.get_window_offset_x()
    offset_y = window_util.get_window_offset_y()
    is_load = True


def click(x, y):
    do_click(x, y, True)


def click_target(x, y):
    do_click(x, y, False)


def do_click(x, y, random_offset_this_time):
    if not is_load:
        do_load()
    real_x = x + offset_x
    real_y = y + offset_y
    if need_random_offset and random_offset_this_time:
        real_x += random.uniform(-5, 5)
        real_y += random.uniform(-5, 5)

    pyautogui.moveTo(real_x, real_y)
    pyautogui.click()


def move_to(x1, y1, x2, y2):
    do_move_to(x1, y1, x2, y2, True)


def move_to_target(x1, y1, x2, y2):
    do_move_to(x1, y1, x2, y2, False)


def do_move_to(x1, y1, x2, y2, random_offset_this_time):
    if not is_load:
        do_load()
    real_x1 = x1 + offset_x
    real_y1 = y1 + offset_y
    real_x2 = x2 + offset_x
    real_y2 = y2 + offset_y
    if random_offset_this_time:
        real_x1 += random.uniform(-5, 5)
        real_y1 += random.uniform(-5, 5)
        real_x2 += random.uniform(-5, 5)
        real_y2 += random.uniform(-5, 5)
    pyautogui.moveTo(real_x1, real_y1)
    pyautogui.mouseDown()  # 按下鼠标
    pyautogui.moveTo(real_x2, real_y2)  # 拖动到新的位置
    pyautogui.mouseUp()  # 松开鼠标


def get_color(x, y):
    if not is_load:
        do_load()
    pyautogui.moveTo(x, y)


def rgb_to_hex(rgb):
    """将 RGB 值转换为 #RRGGBB 格式的十六进制颜色代码"""
    return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"


def get_color_at_coordinate(x, y):
    """
    获取单个点的颜色值。

    :param x: 点的 x 坐标
    :param y: 点的 y 坐标
    :return: 该点的颜色值，格式为 #RRGGBB
    """
    if not is_load:
        do_load()
    # 使用 ImageGrab 截取屏幕
    screenshot = ImageGrab.grab()

    real_x = x + offset_x
    real_y = y + offset_y
    rgb_value = screenshot.getpixel((real_x, real_y))

    # 转换为十六进制颜色值
    return rgb_to_hex(rgb_value)


def get_colors_at_coordinates(coordinates):
    """
    获取多个坐标点的颜色值。

    :param coordinates: 坐标列表，每个元素为 (x, y)
    :return: 包含颜色值的数组，每个值为 #RRGGBB 格式的十六进制颜色代码
    """
    if not is_load:
        do_load()

    # 使用 ImageGrab 截取屏幕
    screenshot = ImageGrab.grab()

    colors = []
    for x, y in coordinates:
        # 计算实际坐标
        real_x = x + offset_x
        real_y = y + offset_y
        # 获取像素颜色值
        rgb_value = screenshot.getpixel((real_x, real_y))
        # 转换为十六进制颜色值并加入结果列表
        colors.append(rgb_to_hex(rgb_value))

    return colors


if __name__ == "__main__":
    # 示例调用
    coordinates = [(100, 200), (150, 250), (200, 300)]
    colors = get_colors_at_coordinates(coordinates)
    print("获取到的颜色值:", colors)
