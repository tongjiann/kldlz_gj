import load_config
import ui_util


def get_hero_valid_checking_color():
    coordinate_info = load_config.get_coordinate_info()
    # 定义 X 和 Y 范围
    x_range = range(1, 4)
    y_range = range(1, 7)
    xy_array = [f"{x}-{y}" for y in y_range for x in x_range]
    map_data = coordinate_info["战斗界面"]["英雄检查点"]
    check_points = [(map_data['1']["x"], map_data['1']["y"]),
                    (map_data['2']["x"], map_data['2']["y"]),
                    (map_data['3']["x"], map_data['3']["y"]),
                    (map_data['4']["x"], map_data['4']["y"])]

    # 提取格子地图
    grid_map = coordinate_info.get("战斗界面", {}).get("格子", {})

    # 遍历所有坐标
    for grid in xy_array:
        # 跳过不存在的格子
        if grid not in grid_map:
            continue

        # 获取格子坐标
        x, y = grid_map[grid]["x"], grid_map[grid]["y"]

        # 执行点击操作
        ui_util.click(x, y)

        # 获取验证点的颜色
        color = ui_util.get_color_at_coordinate(*(
            [map_data["合法性检测"]["x"],
             map_data["合法性检测"]["y"]]))

        # 校验颜色是否匹配
        if map_data["合法性检测"]["color"] == color:
            # 获取当前英雄的颜色信息作为键值
            key = "".join(ui_util.get_color_at_coordinate(x, y) for x, y in check_points)
            print(grid, key)


if __name__ == '__main__':
    get_hero_valid_checking_color()
