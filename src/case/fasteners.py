"""
螺丝孔系统 - 处理键盘外壳的螺丝孔
"""
from ..lib import *
from ..keyboard_utils import point_on_grid, bottom_height

# 螺丝孔配置
screw_insert_height = 2.5
screw_insert_bottom_radius = 5.31 / 2.0
screw_insert_top_radius = 5.1 / 2
screw_insert_width = 2

# 螺丝孔头部配置
screw_head_height = 1.0
screw_head_radius = 5.5 / 2
screw_hole_radius = 1.7

# 螺丝孔几何体
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
    from ..keyboard_utils import num_cols, max_num_rows, num_rows_for_col
    return union(
        screw_insert(2, 0, shape, -5.3, 5.3), 
        screw_insert(num_cols - 1, 0, shape, 6.7, 4.7),  
        screw_insert(num_cols - 1, num_rows_for_col(num_cols - 1), shape, -31, 14), 
        screw_insert(0, 0, shape, -4.7, 5.3),  
        # 底部两个螺丝孔
        screw_insert(1, max_num_rows + 1, shape, -9.7, 3.7),  
        screw_insert(0, max_num_rows - 1, shape, -13.3, 1.7),  
    )

def get_screw_head_shape(for_bottom_plate=True):
    """获取螺丝头部形状"""
    if for_bottom_plate:
        return cylinderr1r2(screw_head_radius, screw_head_radius, screw_head_height)
    return screw_insert_inner

def get_screw_hole_shape():
    """获取螺丝孔形状"""
    return cylinderr1r2(screw_hole_radius, screw_hole_radius, bottom_height)
