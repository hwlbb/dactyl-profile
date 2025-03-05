"""
外壳墙壁 - 处理键盘外壳边缘
"""
from ..lib import *
from ..keyboard_utils import should_include_risers
from ..supports import (
    square_idx_tl, square_idx_tr, square_idx_bl, square_idx_br,
    wall_connect
)

def case_walls():
    """创建键盘外壳的墙壁"""
    from ..keyboard_utils import num_cols, num_rows_for_col
    
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

def wall_shape():
    """创建墙壁的2D形状用于底板"""
    from ..thumb_cluster import thumb_walls, thumb_to_body_connectors
    
    walls_3d = union(
        case_walls(),
        thumb_walls(),
        thumb_to_body_connectors(),
    )

    walls_2d = offset(0.4)(project(cut=True))(translate(0, 0, -0.1)(walls_3d))
    return walls_2d
