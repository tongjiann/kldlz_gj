import Quartz
from time import time

import log_util

window_title = "快来当领主"
refresh_time = 5000
last_updated = 0
window = None
logger = log_util.Logger()


# This function retrieves a list of all windows with their titles
def get_window_list():
    window_list = []
    window_info_list = Quartz.CGWindowListCopyWindowInfo(Quartz.kCGWindowListOptionOnScreenOnly, Quartz.kCGNullWindowID)
    for window_info in window_info_list:
        window_list.append(window_info)
    return window_list


# This function will look for a window with a specific title
def get_window_with_title(title):
    for window in get_window_list():
        window_title = window.get('kCGWindowOwnerName', 'No Title')
        if window_title == title:
            return window
    return None


def update_window_info_if_need():
    timestamp = int(time())
    global window
    global last_updated
    if last_updated is None or timestamp - last_updated > refresh_time:
        logger.info("重新获取窗口")
        window = get_window_with_title(window_title)
        last_updated = timestamp


def get_window_offset_x():
    global window
    update_window_info_if_need()
    if window is None:
        raise LogicalError("未找到指定窗口")
    return window['kCGWindowBounds']["X"]


def get_window_offset_y():
    global window
    update_window_info_if_need()
    if window is None:
        raise LogicalError("未找到指定窗口")
    return window['kCGWindowBounds']["Y"]


# 自定义异常类
class LogicalError(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message
