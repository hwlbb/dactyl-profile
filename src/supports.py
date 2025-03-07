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
from .shapes import (
    SWITCH_RISER_RADIUS, SWITCH_RISER_HEIGHT,
    switch_riser_raw_dot, switch_riser_post, top_dot
)

# 支柱相关常量
OUTER_POST_DELTA = keyhole_size / 2 + switch_rim_thickness
INNER_POST_DELTA = keyhole_size / 2 + post_rad
SWITCH_RISER_OFFSET = 9.8 + SWITCH_RISER_RADIUS

# 角落索引常量，使代码更易读
square_idx_tl = [1, 0]  # 左上角
square_idx_tr = [1, 1]  # 右上角
square_idx_bl = [0, 0]  # 左下角
square_idx_br = [0, 1]  # 右下角

# ===== 支撑柱系统 =====
class WebPostSystem:
    """支撑柱系统，处理支撑柱的创建和管理"""
    
    def __init__(self):
        # 创建基础支撑柱
        self.web_post = translate(-post_rad, -post_rad, switch_thickness - web_thickness)(
            cube(post_width, post_width, web_thickness))
        self.short_web_post = translate(-post_rad, -post_rad, 0)(
            cube(post_width, post_width, post_width))
        
        # 创建支撑柱矩阵
        self.web_posts = self._create_post_matrix(OUTER_POST_DELTA, self.web_post)
        self.short_web_posts = self._create_post_matrix(OUTER_POST_DELTA, self.short_web_post)
        self.inner_web_posts = self._create_post_matrix(INNER_POST_DELTA, self.web_post)
        self.short_inner_web_posts = self._create_post_matrix(INNER_POST_DELTA, self.short_web_post)
        
        # 创建常用边缘
        self.post_left_edge = [self.get_post(square_idx_bl), self.get_post(square_idx_tl)]
        self.post_top_edge = [self.get_post(square_idx_tl), self.get_post(square_idx_tr)]
        self.post_right_edge = [self.get_post(square_idx_tr), self.get_post(square_idx_br)]
        self.post_bot_edge = [self.get_post(square_idx_br), self.get_post(square_idx_bl)]
        
        # 创建开关升高器矩阵
        self.switch_riser_offset_square = self._create_offset_matrix(SWITCH_RISER_OFFSET)
    
    def _create_post_matrix(self, delta, post_shape):
        """创建指定偏移量和形状的支撑柱矩阵"""
        offset_matrix = self._create_offset_matrix(delta)
        return [[t(post_shape) for t in row] for row in offset_matrix]
    
    def _create_offset_matrix(self, delta):
        """创建偏移变换矩阵"""
        corners = [
            [[-1, -1], [1, -1]],  # 左下, 右下
            [[-1, 1],  [1, 1]]    # 左上, 右上
        ]
        return [[translate(x * delta, y * delta, 0) for x, y in row] for row in corners]
    
    def get_post(self, idx):
        """获取指定位置的支撑柱"""
        return self.web_posts[idx[0]][idx[1]]
    
    def get_inner_post(self, idx):
        """获取指定位置的内部支撑柱"""
        return self.inner_web_posts[idx[0]][idx[1]]
    
    def get_short_post(self, idx):
        """获取指定位置的短支撑柱"""
        return self.short_web_posts[idx[0]][idx[1]]
    
    def get_short_inner_post(self, idx):
        """获取指定位置的短内部支撑柱"""
        return self.short_inner_web_posts[idx[0]][idx[1]]
    
    def get_riser_offset(self, idx):
        """获取升高器偏移变换"""
        return self.switch_riser_offset_square[idx[0]][idx[1]]

# 创建全局支撑柱系统实例
post_system = WebPostSystem()

# 为保持向后兼容，创建别名
web_post = post_system.web_post
web_post_tr = post_system.get_post(square_idx_tr)
web_post_tl = post_system.get_post(square_idx_tl)
web_post_br = post_system.get_post(square_idx_br)
web_post_bl = post_system.get_post(square_idx_bl)
web_posts = post_system.web_posts
post_left_edge = post_system.post_left_edge
post_top_edge = post_system.post_top_edge
post_right_edge = post_system.post_right_edge
post_bot_edge = post_system.post_bot_edge
switch_riser_offset_square = post_system.switch_riser_offset_square

# ===== 特殊位置配置 =====
def get_riser_is_connector(rc1, idx1, rc2, idx2):
    """确定是否应该在两个位置之间创建连接器"""
    if rc1 == [0, 3] and rc2 == [0, 4]:
        return False
    return True

def get_riser_offset_delta(row_col, idx):
    """获取特定位置的升高器偏移量"""
    # 特殊位置配置表
    special_positions = {
        # [row, col, idx] : [dx, dy]
        (0, 1, tuple(square_idx_tr)): [-2.1, 0],
        (0, 3, tuple(square_idx_tl)): [2.1, 0],
        (0, 3, tuple(square_idx_tr)): [0, 0],
        (0, 4, tuple(square_idx_tl)): [1.5, 0],
        (2, 4, tuple(square_idx_bl)): [2.9, 0],
        (3, 2, tuple(square_idx_br)): [-2.9, 0],
        (2, 1, tuple(square_idx_br)): [-1.5, 0],
    }
    
    key = (row_col[0], row_col[1], tuple(idx))
    return special_positions.get(key)

# ===== 墙壁连接函数 =====
def make_offsetter(idx, delta):
    """创建偏移器函数"""
    offsetter = post_system.get_riser_offset(idx)
    
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
    
    if include_risers:
        shapes.append(hull(place_fn1(post1), place_fn2(post2)))
    
    if connectors:
        shapes.append(
            hull(
                place_fn1(union(offsetter1(web_post), post_system.get_post(idx1))),
                place_fn2(union(offsetter2(web_post), post_system.get_post(idx2))),
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

def wall_connect(row1, col1, idx1, row2, col2, idx2, **kwargs):
    """连接两个位置的墙壁"""
    place_fn1 = place_on_grid(row1, col1)
    place_fn2 = place_on_grid(row2, col2)
    
    delta1 = get_riser_offset_delta([row1, col1], idx1)
    delta2 = get_riser_offset_delta([row2, col2], idx2)
    
    connectors = get_riser_is_connector([row1, col1], idx1, [row2, col2], idx2)
    include_risers = kwargs.pop('include_risers', True)
    
    return wall_connect_from_placer(place_fn1, idx1, place_fn2, idx2, 
                                  delta1=delta1, delta2=delta2, 
                                  connectors=connectors, 
                                  include_risers=include_risers, 
                                  **kwargs)

# ===== 连接器函数 =====
def make_edge_connection(r1, c1, e1, r2, c2, e2):
    """连接两个位置的边缘"""
    posts1 = [grid_position(r1, c1, e) for e in e1]
    posts2 = [grid_position(r2, c2, e) for e in e2]
    return hull(*posts1, *posts2)

def create_horizontal_connectors():
    """创建水平连接器"""
    connectors = []
    
    for col in range(num_cols - 1):
        for row in range(max_num_rows):
            if does_coord_exist(row, col) and does_coord_exist(row, col + 1):
                if (row, col) == (0, 3):
                    right_edge = [translate(1, 1, 0)(web_post_tr), translate(0, 1, 0)(web_post_tr), web_post_br]
                else:
                    right_edge = post_right_edge
                connectors.append(make_edge_connection(row, col, right_edge, row, col + 1, post_left_edge))
    
    return connectors

def create_vertical_connectors():
    """创建垂直连接器"""
    connectors = []
    
    for col in range(num_cols):
        for row in range(max_num_rows - 1):
            if does_coord_exist(row, col) and does_coord_exist(row + 1, col):
                connectors.append(make_edge_connection(row, col, post_bot_edge, row + 1, col, post_top_edge))
    
    return connectors

def create_height_change_connectors():
    """创建高度变化连接器"""
    connectors = []
    
    # 处理高度增加的情况
    for col in range(num_cols - 1):
        row = num_rows_for_col(col) - 1
        next_col = col + 1
        next_row = num_rows_for_col(next_col) - 1
        
        # 下一列比当前列多一行
        if next_row == row + 1:
            this_t = place_on_grid(row, col)
            next_t = place_on_grid(next_row, next_col)
            this_level_t = place_on_grid(row, next_col)
            connectors.append(
                hull(
                    this_t(web_post_br),
                    this_level_t(web_post_bl),
                    next_t(web_post_tl),
                )
            )
            connectors.append(
                hull(
                    this_t(web_post_br),
                    next_t(web_post_tl),
                    next_t(web_post_bl),
                )
            )
        
        # 下一列比当前列少一行
        if next_row == row - 1:
            this_t = place_on_grid(row, col)
            next_t = place_on_grid(next_row, next_col)
            this_level_t = place_on_grid(next_row, col)
            connectors.append(
                hull(
                    this_t(web_post_tr),
                    this_level_t(web_post_br),
                    next_t(web_post_bl),
                )
            )
            connectors.append(
                hull(
                    this_t(web_post_tr),
                    this_t(web_post_br),
                    next_t(web_post_bl),
                )
            )
    
    return connectors

def create_diagonal_connectors():
    """创建对角连接器"""
    connectors = []
    
    def does_diag_exist(row, col):
        """检查2x2区域内所有位置是否都存在"""
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
                connectors.append(hull(p1, p2, p3, p4))
    
    return connectors

def connectors():
    """创建连接键位之间的结构"""
    all_connectors = []
    
    # 添加各种类型的连接器
    all_connectors.extend(create_horizontal_connectors())
    all_connectors.extend(create_vertical_connectors())
    all_connectors.extend(create_height_change_connectors())
    all_connectors.extend(create_diagonal_connectors())
    
    return union(*all_connectors)

# 保留原有的测试函数
def post_test():
    """测试所有支撑柱的显示"""
    return union(
        *[y for x in post_system.short_web_posts for y in x],
    )

# 为保持向后兼容，定义必要的函数
def get_in_square(square, idx):
    """获取正方形中指定位置的元素"""
    return square[idx[0]][idx[1]]

def get_web_post(idx):
    """获取指定索引的支撑柱"""
    return post_system.get_post(idx)