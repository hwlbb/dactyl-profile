"""
重置开关 - 处理键盘的重置按钮
"""
from ..lib import *
from ..keyboard_utils import point_on_grid, bottom_height

# 重置开关尺寸
reset_switch_hole_height = 4.2
reset_switch_width = 6.0
reset_switch_hole_depth = 6.5
reset_switch_hole_back = 5.0
reset_switch_hole_radius = 4.3 / 2
reset_switch_total_depth = reset_switch_hole_depth + reset_switch_hole_back
reset_switch_total_height = reset_switch_hole_height + 2 * bottom_height

def unplaced_reset_switch_body():
    """创建重置开关的主体"""
    shape = cube(reset_switch_width, reset_switch_total_depth, reset_switch_total_height, center=True)
    return translate(0, 0, reset_switch_total_height / 2)(shape)

def unplaced_reset_switch_body_hole():
    """创建重置开关的孔"""
    rect = translate(0, -reset_switch_hole_back / 2.0, reset_switch_hole_height / 2.0 + bottom_height)(
            cube(reset_switch_width + 0.2, reset_switch_hole_depth, reset_switch_hole_height, center=True)
    )
    cyl = translate(0, -reset_switch_hole_back / 2, bottom_height / 2)(
        cylinder(reset_switch_hole_radius, bottom_height, center=True))

    return union(rect, cyl)

def place_reset_switch_shape(shape):
    """放置重置开关在正确位置"""
    base_point = point_on_grid(1, 1, 0, 0, 0)
    return translate(base_point[0], base_point[1], 0)(shape)

# 创建放置好的重置开关
reset_switch_body = place_reset_switch_shape(unplaced_reset_switch_body())
reset_switch_body_hole = place_reset_switch_shape(unplaced_reset_switch_body_hole())
