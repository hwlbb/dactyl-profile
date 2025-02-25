"""
支撑结构 - 提供键盘底座和连接结构的相关函数
"""
from .lib import *
from .shapes import *
from .keyboard_utils import (
    post_width, post_rad, web_thickness, switch_thickness,
    keyhole_size, switch_rim_thickness, does_coord_exist,
    bottom_hull, grid_position, place_on_grid, num_rows_for_col,
    max_num_rows, num_cols, should_include_risers
)
# 直接导入shapes中定义的常量和变量
from .shapes import (
    SWITCH_RISER_RADIUS, SWITCH_RISER_HEIGHT,
    switch_riser_raw_dot, switch_riser_post, top_dot
)

# 创建网格支撑结构
web_post = translate(-post_rad, -post_rad, switch_thickness - web_thickness)(
    cube(post_width, post_width, web_thickness))
short_web_post = translate(-post_rad, -post_rad, 0)(
    cube(post_width, post_width, post_width))

SQUARE_OFFSET_IDXS = [
    [[-1, -1], [1, -1]],
    [[-1, 1], [1, 1]],
]

def square_apply(square, fn):
    """对正方形的每个位置应用函数"""
    return [[fn(x) for x in y] for y in square]

def square_translater_at_offset(offset):
    """创建在给定偏移量处的平移函数"""
    def fn(idx):
        return translate(idx[0] * offset, idx[1] * offset, 0)

    return square_apply(SQUARE_OFFSET_IDXS, fn)

def apply_translate_square(square, shape):
    """应用平移矩阵到形状"""
    def fn(translator):
        return translator(shape)
    return square_apply(square, fn)

# 支柱偏移量
outer_post_delta = keyhole_size / 2 + switch_rim_thickness

# 支柱布局的基础位置
outer_post_translate_square = square_translater_at_offset(outer_post_delta)

# 创建支撑柱位置
web_post_tr = translate(outer_post_delta, outer_post_delta, 0)(web_post)
web_post_tl = translate(-outer_post_delta, outer_post_delta, 0)(web_post)
web_post_br = translate(outer_post_delta, -outer_post_delta, 0)(web_post)
web_post_bl = translate(-outer_post_delta, -outer_post_delta, 0)(web_post)

# 应用到全部位置
web_posts = apply_translate_square(outer_post_translate_square, web_post)
short_web_posts = apply_translate_square(outer_post_translate_square, short_web_post)

# 内部支柱
inner_post_delta = keyhole_size / 2 + post_rad
inner_post_translate_square = square_translater_at_offset(inner_post_delta)

inner_web_posts = apply_translate_square(inner_post_translate_square, web_post)
short_inner_web_posts = apply_translate_square(inner_post_translate_square, short_web_post)

# 边缘索引
post_left_edge_indexes = [[0, 0], [1, 0]]
post_top_edge_indexes = [[1, 0], [1, 1]]
post_right_edge_indexes = [[1, 1], [0, 1]]
post_bot_edge_indexes = [[0, 1], [0, 0]]

# 角落索引
square_idx_tl = [1, 0]
square_idx_tr = [1, 1]
square_idx_bl = [0, 0]
square_idx_br = [0, 1]

# 开关升高器的偏移量和形状
SWITCH_RISER_OFFSET = 9.8 + SWITCH_RISER_RADIUS
switch_riser_offset_square = square_translater_at_offset(SWITCH_RISER_OFFSET)

def get_web_post(idx):
    """获取指定索引的支撑柱"""
    return web_posts[idx[0]][idx[1]]

# 创建边缘
post_left_edge = [get_web_post(e) for e in post_left_edge_indexes]
post_top_edge = [get_web_post(e) for e in post_top_edge_indexes]
post_right_edge = [get_web_post(e) for e in post_right_edge_indexes]
post_bot_edge = [get_web_post(e) for e in post_bot_edge_indexes]

def get_in_square(square, idx):
    """获取正方形中指定位置的元素"""
    return square[idx[0]][idx[1]]

def get_inner_web_post(idx):
    """获取内部支撑柱"""
    return get_in_square(inner_web_posts, idx)

def get_short_web_post(idx):
    """获取短支撑柱"""
    return get_in_square(short_web_posts, idx)

def get_short_inner_web_post(idx):
    """获取短内部支撑柱"""
    return get_in_square(short_inner_web_posts, idx)

def get_riser_is_connector(rc1, idx1, rc2, idx2):
    """确定是否应该在两个位置之间创建连接器"""
    if rc1 == [0, 3] and rc2 == [0, 4]:
        return False
    return True

def get_riser_offset_delta(row_col, idx):
    """获取特定位置的升高器偏移量"""
    if row_col == [0, 1] and idx == square_idx_tr:
        return [-2.1, 0]
    if row_col == [0, 3] and idx == square_idx_tl:
        return [2.1, 0]
    if row_col == [0, 3] and idx == square_idx_tr:
        return [0, 0]
    if row_col == [0, 4] and idx == square_idx_tl:
        return [1.5, 0]
    if row_col == [2, 4] and idx == square_idx_bl:
        return [2.9, 0]
    if row_col == [3, 2] and idx == square_idx_br:
        return [-2.9, 0]
    if row_col == [2, 1] and idx == square_idx_br:
        return [-1.5, 0]
    else:
        return None

def wall_connect(row1, col1, idx1, row2, col2, idx2, **kwargs):
    """连接两个位置的墙壁"""
    place_fn1 = place_on_grid(row1, col1)
    place_fn2 = place_on_grid(row2, col2)

    delta1 = get_riser_offset_delta([row1, col1], idx1)
    delta2 = get_riser_offset_delta([row2, col2], idx2)

    connectors = get_riser_is_connector([row1, col1], idx1, [row2, col2], idx2)

    # 获取should_include_risers值，如果没有提供，则使用True作为默认值（这是关键修改点）
    include_risers = kwargs.pop('include_risers', True)
    
    return wall_connect_from_placer(place_fn1, idx1, place_fn2, idx2, 
                                   delta1=delta1, delta2=delta2, 
                                   connectors=connectors, 
                                   include_risers=include_risers, 
                                   **kwargs)

def make_offsetter(idx, delta):
    """创建偏移器函数"""
    offsetter = get_in_square(switch_riser_offset_square, idx)

    if delta:
        z = 0
        if len(delta) == 3:
            z = delta[2]
        offsetter = translate(delta[0], delta[1], z)(offsetter)
    return offsetter

def wall_connect_from_placer(place_fn1, idx1, place_fn2, idx2, *, delta1=None, delta2=None, connectors=True, walls=True, include_risers=True):
    """连接两个位置的墙壁（基于定位函数）"""
    offsetter1 = make_offsetter(idx1, delta1)
    offsetter2 = make_offsetter(idx2, delta2)

    post1 = offsetter1(switch_riser_post)
    post2 = offsetter2(switch_riser_post)

    shapes = []

    # 使用参数include_risers代替全局变量
    if include_risers:
        shapes.append(hull(place_fn1(post1), place_fn2(post2)))

    if connectors:
        shapes.append(
            hull(
                place_fn1(union(offsetter1(web_post), get_in_square(web_posts, idx1))),
                place_fn2(union(offsetter2(web_post), get_in_square(web_posts, idx2))),
            )
        )

    if walls:
        shapes.append(
            bottom_hull(hull(
                place_fn1(offsetter1(switch_riser_raw_dot)),
                place_fn2(offsetter2(switch_riser_raw_dot)),
            ))
        )

    return union(*shapes)

def connectors():
    """创建连接键位之间的结构"""
    def make_edge_connection(r1, c1, e1, r2, c2, e2):
        """连接两个位置的边缘"""
        posts1 = [grid_position(r1, c1, e) for e in e1]
        posts2 = [grid_position(r2, c2, e) for e in e2]
        return hull(*posts1, *posts2)

    all_connectors = []
    
    # 水平连接器
    for col in range(num_cols - 1):
        for row in range(max_num_rows):
            if does_coord_exist(row, col) and does_coord_exist(row, col + 1):
                if (row, col) == (0, 3):
                    right_edge = [translate(1, 1, 0)(web_post_tr), translate(0, 1, 0)(web_post_tr), web_post_br]
                else:
                    right_edge = post_right_edge
                all_connectors.append(make_edge_connection(row, col, right_edge, row, col + 1, post_left_edge))

    # 垂直连接器
    for col in range(num_cols):
        for row in range(max_num_rows - 1):
            if does_coord_exist(row, col) and does_coord_exist(row + 1, col):
                all_connectors.append(make_edge_connection(row, col, post_bot_edge, row + 1, col, post_top_edge))

    # 特殊情况的连接器 - 处理高度变化
    for col in range(num_cols - 1):
        row = num_rows_for_col(col) - 1
        next_col = col + 1
        next_row = num_rows_for_col(next_col) - 1
        
        if next_row == row + 1:
            this_t = place_on_grid(row, col)
            next_t = place_on_grid(next_row, next_col)
            this_level_t = place_on_grid(row, next_col)
            all_connectors.append(
                hull(
                    this_t(web_post_br),
                    this_level_t(web_post_bl),
                    next_t(web_post_tl),
                )
            )
            all_connectors.append(
                hull(
                    this_t(web_post_br),
                    next_t(web_post_tl),
                    next_t(web_post_bl),
                )
            )
        
        if next_row == row - 1:
            this_t = place_on_grid(row, col)
            next_t = place_on_grid(next_row, next_col)
            this_level_t = place_on_grid(next_row, col)

            all_connectors.append(
                hull(
                    this_t(web_post_tr),
                    this_level_t(web_post_br),
                    next_t(web_post_bl),
                )
            )

            all_connectors.append(
                hull(
                    this_t(web_post_tr),
                    this_t(web_post_br),
                    next_t(web_post_bl),
                )
            )

    # 对角连接器
    def does_diag_exist(row, col):
        for dr in [0, 1]:
            for dc in [0, 1]:
                if not does_coord_exist(row + dr, col + dc):
                    return False
        return True

    for col in range(num_cols - 1):
        for row in range(max_num_rows - 1):
            if does_diag_exist(row, col):
                p1 = grid_position(row, col, web_post_br)
                p2 = grid_position(row+1, col, web_post_tr)
                p3 = grid_position(row+1, col+1, web_post_tl)
                p4 = grid_position(row, col+1, web_post_bl)
                all_connectors.append(hull(p1, p2, p3, p4))

    return union(*all_connectors)

def post_test():
    """测试所有支撑柱的显示"""
    return union(
        *[y for x in short_web_posts for y in x],
    )