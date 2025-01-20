import pyautogui

# 移动鼠标到屏幕的指定位置（x=100, y=200）
pyautogui.moveTo(100, 200, duration=1)  # duration 是移动的时间（秒）

# 鼠标点击
pyautogui.click()

# 鼠标双击
pyautogui.doubleClick()

# 鼠标右击
pyautogui.rightClick()

# 拖动鼠标
pyautogui.moveTo(500, 500, duration=1)  # 先移动到目标位置
pyautogui.mouseDown()  # 按下鼠标
pyautogui.moveTo(700, 700, duration=1)  # 拖动到新的位置
pyautogui.mouseUp()  # 松开鼠标
