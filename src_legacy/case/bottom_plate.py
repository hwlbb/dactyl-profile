"""
底板系统 - 处理键盘底板和减重孔
"""
from ..lib import *
from ..keyboard_utils import (
    should_include_risers, point_on_grid, bottom_height
)
from ..supports import connectors
from ..switches import filled_switches  # 修改这行，导入函数而不是对象
from .walls import wall_shape, case_walls  # 也需要导入case_walls函数
from .reset_switch import reset_switch_body, reset_switch_body_hole
from .fasteners import screw_insert_all_shapes, get_screw_head_shape, get_screw_hole_shape

# 重量块的配置
weight_width = 19.5
weight_height = 16.5
weight_z_offset = 0.5

def weight_shape():
    """创建重量块形状"""
    return translate(0, 0, 1.5 + weight_z_offset)(cube(weight_width, weight_height, 3, center=True))

def weight_shape_vert():
    """创建垂直的重量块形状"""
    return rotate_z(90)(weight_shape())

def place_weight_hole(x, y):
    """在指定位置放置重量块孔"""
    return translate(x, y, 0)(weight_shape())

def bottom_weight_cutouts():
    """创建底板上的重量块开孔"""
    from ..keyboard_utils import point_on_grid, num_cols
    
    shapes = []

    base_point = point_on_grid(0, num_cols - 1, 0, 0, 0)
    base_x = base_point[0] - 9
    base_y = base_point[1] - 4

    space_between = 1
    offsets = space_between + weight_width
    offsets_y = space_between + weight_height

    r3_y = base_y - 2 * offsets_y
    topr = base_y + offsets_y

    # 第一行重量块
    for x in range(2):
        shapes.append(place_weight_hole(1 + base_x - offsets * x, base_y))
    for x in range(3, 4):
        shapes.append(place_weight_hole(base_x - offsets * x + 2, base_y))
    for x in range(4, 5):
        shapes.append(place_weight_hole(base_x - offsets * x - 8, base_y))

    # 第二行重量块 
    for x in range(2, 5):
        shapes.append(place_weight_hole(base_x - offsets * x - 4, base_y - offsets_y))

    # 第三行重量块
    for x in range(5):
        shapes.append(place_weight_hole(base_x - offsets * x, base_y - 2 * offsets_y))

    # 顶部重量块
    shapes.append(place_weight_hole(base_x - offsets * 2, topr))
    shapes.append(place_weight_hole(base_x - offsets * 3, topr))

    # 拇指区域重量块
    base_thumb_x = base_x - offsets * 4 + 5
    base_thumb_y = base_y - offsets_y * 3 - weight_width + weight_height + 1

    angled_shape = rotate_z(107)(weight_shape())
    shapes.append(translate(base_thumb_x - offsets_y - 0.4, base_thumb_y - 9.5, 0)(angled_shape))
    shapes.append(translate(base_thumb_x - offsets_y + 16, base_thumb_y - 1, 0)(angled_shape))

    return union(*shapes)

def model_outline():
    """创建键盘的整体轮廓"""
    global should_include_risers
    should_include_risers = False
    
    from ..thumb_cluster import (
        filled_thumb_switches, thumb_walls, 
        thumb_connectors, thumb_to_body_connectors
    )

    solid_bottom = project()(union(
        filled_switches(),  # 使用导入的函数
        connectors(),
        case_walls(),  # 确保此函数可用
        filled_thumb_switches(),
        thumb_walls(),
        thumb_connectors(),
        thumb_to_body_connectors(),
    ))

    bottom_2d = difference(solid_bottom, wall_shape())
    return extrude_linear(bottom_height)(bottom_2d)

def bottom_plate():
    """创建键盘底板"""
    return difference(
        union(
            model_outline(),
            reset_switch_body,
            # screw_insert_all_shapes(screw_insert_outer),
        ),
        union(
            screw_insert_all_shapes(get_screw_head_shape()),
            screw_insert_all_shapes(get_screw_hole_shape()),
            bottom_weight_cutouts(),
            reset_switch_body_hole,
        )
    )
