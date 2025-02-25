"""
外壳构建 - 处理键盘外壳和底板的构建
"""
from .lib import *
from .shapes import *
from .keyboard_utils import (
    should_include_risers, blocker, point_on_grid, 
    bottom_height, bottom_hull, keyswitch_width
)
from .switches import single_switch, filled_switch, sa_cap
from .supports import (
    connectors, square_idx_tl, square_idx_tr, square_idx_bl, square_idx_br,
    get_in_square, wall_connect
)

screw_insert_height = 2.5
screw_insert_bottom_radius = 5.31 / 2.0
screw_insert_top_radius = 5.1 / 2

screw_insert_width = 2

# 螺丝孔
screw_insert_outer = translate(0, 0, bottom_height)(
    cylinderr1r2(screw_insert_bottom_radius + screw_insert_width, 
                screw_insert_top_radius + screw_insert_width, 
                screw_insert_height + screw_insert_width))

screw_insert_inner = translate(0, 0, bottom_height)(
    cylinderr1r2(screw_insert_bottom_radius, screw_insert_top_radius, screw_insert_height))

def screw_insert(col, row, shape, ox, oy):
    """在指定位置创建螺丝孔"""
    postiion = point_on_grid(row, col, 0, 0, 0)
    postiion[2] = 0
    postiion[0] += ox
    postiion[1] += oy
    return translate(*postiion)(shape)

def screw_insert_all_shapes(shape):
    """创建所有螺丝孔"""
    from .keyboard_utils import num_cols, max_num_rows, num_rows_for_col
    return union(
        screw_insert(2, 0, shape, -5.3, 5.3), 
        screw_insert(num_cols - 1, 0, shape, 6.7, 4.7),  
        screw_insert(num_cols - 1, num_rows_for_col(num_cols - 1), shape, -31, 14), 
        screw_insert(0, 0, shape, -4.7, 5.3),  
        # 底部两个螺丝孔
        screw_insert(1, max_num_rows + 1, shape, -9.7, 3.7),  
        screw_insert(0, max_num_rows - 1, shape, -13.3, 1.7),  
    )

# TRRS连接器（用于两半键盘之间的连接）
trrs_holder_size = [6.0, 11.0, 7.0]
trrs_hole_size = [2.6, 10.0]
trrs_holder_thickness = 2.5
trrs_front_thickness = 1.8

def trrs_key_holder_position():
    """定位TRRS接口的位置"""
    base_place = point_on_grid(0, 0, 0, keyswitch_width / 2, 0)
    return [base_place[0] + 3, base_place[1] + 2.43, 8.5]

def trrs_holder():
    """创建TRRS接口支架"""
    shape = cube(
        trrs_holder_size[0] + trrs_holder_thickness,
        trrs_holder_size[1] + trrs_front_thickness,
        trrs_holder_size[2] + trrs_holder_thickness * 2,
    )

    placed_shape = translate(
            -trrs_holder_size[0] / 2,
            -trrs_holder_size[1],
            -(trrs_holder_size[2] / 2 + trrs_holder_thickness),
    )(shape)

    return translate(*trrs_key_holder_position())(placed_shape)

def trrs_holder_hole():
    """创建TRRS接口孔"""
    rect_hole = cube(*trrs_holder_size)
    rect_hole = translate(
            -trrs_holder_size[0] / 2,
            -trrs_holder_size[1],
            -trrs_holder_size[2] / 2,
        )(rect_hole)

    cylinder_hole = cylinder(*trrs_hole_size, segments=30)
    cylinder_hole = rotate_x(90)(cylinder_hole)
    cylinder_hole = translate(0, 5, 0)(cylinder_hole)

    return translate(*trrs_key_holder_position())(union(rect_hole, cylinder_hole))

# USB连接器
usb_holder_hole_dims = [6.5, 15.0, 9.212]
usb_holder_thickness = 2.0

def usb_holder_position():
    """定位USB接口的位置"""
    base_place = point_on_grid(0, 0, 0, keyswitch_width / 2, 0)
    return [base_place[0] + 13, base_place[1], 9]

def usb_holder_rim():
    """创建USB接口支架"""
    base_shape = cube(
        usb_holder_hole_dims[0] + usb_holder_thickness * 2,
        usb_holder_thickness * 2,
        usb_holder_hole_dims[2] + usb_holder_thickness * 2,
    )

    placed_shape = translate(
        -usb_holder_hole_dims[0] / 2 - usb_holder_thickness,
        0,
        -usb_holder_hole_dims[2] / 2 - usb_holder_thickness,
    )(base_shape)

    return translate(*usb_holder_position())(placed_shape)

def usb_holder_hole():
    """创建USB接口孔"""
    placed_shape = translate(
        -usb_holder_hole_dims[0] / 2,
        -usb_holder_hole_dims[1] / 2,
        -usb_holder_hole_dims[2] / 2,
    )(cube(*usb_holder_hole_dims))

    return translate(*usb_holder_position())(placed_shape)

# 重置开关
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

def case_walls():
    """创建键盘外壳的墙壁"""
    from .keyboard_utils import num_cols, num_rows_for_col
    
    all_shapes = []

    # 顶部墙壁
    for col in range(0, num_cols):
        all_shapes.append(wall_connect(0, col, square_idx_tl, 0, col, square_idx_tr, include_risers=True))
    for col in range(0, num_cols - 1):
        all_shapes.append(wall_connect(0, col, square_idx_tr, 0, col + 1, square_idx_tl, include_risers=True))

    # 右侧墙壁
    max_col = num_cols - 1
    for row in range(0, num_rows_for_col(max_col)):
        all_shapes.append(wall_connect(row, max_col, square_idx_tr, row, max_col, square_idx_br, include_risers=True))
    for row in range(0, num_rows_for_col(max_col) - 1):
        all_shapes.append(wall_connect(row, max_col, square_idx_br, row + 1, max_col, square_idx_tr, include_risers=True))

    # 左侧墙壁
    for row in range(0, num_rows_for_col(0)):
        all_shapes.append(wall_connect(row, 0, square_idx_tl, row, 0, square_idx_bl, include_risers=True))
    for row in range(0, num_rows_for_col(0) - 1):
        all_shapes.append(wall_connect(row, 0, square_idx_bl, row + 1, 0, square_idx_tl, include_risers=True))

    # 底部墙壁
    def include_wall(col):
        return col >= 2

    for col in range(0, num_cols):
        all_shapes.append(wall_connect(num_rows_for_col(col) - 1, col, square_idx_bl, num_rows_for_col(col) - 1, col, square_idx_br, 
                                       walls=include_wall(col), include_risers=True))
    for col in range(0, num_cols - 1):
        all_shapes.append(wall_connect(num_rows_for_col(col) - 1, col, square_idx_br, num_rows_for_col(col + 1) - 1, col + 1, square_idx_bl, 
                                       walls=include_wall(col), include_risers=True))

    return union(*all_shapes)

def all_switches():
    """创建所有按键开关"""
    from .keyboard_utils import all_of_shape
    return union(*all_of_shape(single_switch))

def filled_switches():
    """创建所有填充式按键(没有开孔)"""
    from .keyboard_utils import all_of_shape
    return union(*all_of_shape(filled_switch))

def all_caps():
    """创建所有键帽"""
    from .keyboard_utils import all_of_shape
    return union(*all_of_shape(sa_cap))

def wall_shape():
    """创建墙壁的2D形状用于底板"""
    from .thumb_cluster import thumb_walls, thumb_to_body_connectors
    
    walls_3d = union(
        case_walls(),
        thumb_walls(),
        thumb_to_body_connectors(),
    )

    walls_2d = offset(0.4)(project(cut=True))(translate(0, 0, -0.1)(walls_3d))
    return walls_2d

def model_outline():
    """创建键盘的整体轮廓"""
    global should_include_risers
    should_include_risers = False
    
    from .thumb_cluster import (
        filled_thumb_switches, thumb_walls, 
        thumb_connectors, thumb_to_body_connectors
    )

    solid_bottom = project()(union(
        filled_switches(),
        connectors(),
        case_walls(),
        filled_thumb_switches(),
        thumb_walls(),
        thumb_connectors(),
        thumb_to_body_connectors(),
    ))

    bottom_2d = difference(solid_bottom, wall_shape())
    return extrude_linear(bottom_height)(bottom_2d)

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
    from .keyboard_utils import point_on_grid, num_cols
    
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

def bottom_plate():
    """创建键盘底板"""
    screw_head_height = 1.0
    screw_head_radius = 5.5 / 2
    screw_hole_radius = 1.7
    
    return difference(
        union(
            model_outline(),
            reset_switch_body,
            # screw_insert_all_shapes(screw_insert_outer),
        ),
        union(
            screw_insert_all_shapes(cylinderr1r2(screw_head_radius, screw_head_radius, screw_head_height)),
            screw_insert_all_shapes(cylinderr1r2(screw_hole_radius, screw_hole_radius, bottom_height)),
            bottom_weight_cutouts(),
            reset_switch_body_hole,
        )
    )

def left_bottom_plate():
    """创建左侧键盘底板"""
    return flip_lr()(bottom_plate())

def right_shell():
    """创建右侧键盘外壳"""
    global should_include_risers
    should_include_risers = True
    
    from .thumb_cluster import (
        thumb_switches, thumb_walls, thumb_connectors, 
        thumb_to_body_connectors
    )

    full_proto = difference(
        union(
            all_switches(),
            connectors(),
            case_walls(),
            screw_insert_all_shapes(screw_insert_outer),
            # all_caps(),
            thumb_switches(),
            thumb_walls(),
            thumb_connectors(),
            # thumb_caps(),
            thumb_to_body_connectors(),
            trrs_holder(),
            usb_holder_rim(),
        ),
        union(
            blocker(),
            screw_insert_all_shapes(screw_insert_inner),
            trrs_holder_hole(),
            usb_holder_hole(),
        ))

    return full_proto

def left_shell():
    """创建左侧键盘外壳"""
    return flip_lr()(right_shell())