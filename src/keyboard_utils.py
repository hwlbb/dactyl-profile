"""
键盘工具函数 - 基本的键盘定位和形状操作函数

坐标系说明：
- X轴：从左到右
- Y轴：从近到远（远离使用者方向为正）
- Z轴：从下到上（垂直向上为正）

旋转说明：
- 绕X轴旋转：调整前后倾斜（正值使前部向下倾斜）
- 绕Y轴旋转：调整左右倾斜（正值使中部抬高成帐篷状）
- 绕Z轴旋转：调整水平旋转（正值为顺时针，负值为逆时针）
"""
from math import radians, sin, cos
from .lib import *
from .shapes import *
from . import lib
from . import mat
from .config import KeyboardConfig

# 初始化配置
config = KeyboardConfig.create_default()

# 使用配置中的值
switch_thickness = config.switch_thickness
switch_rim_thickness = config.switch_rim_thickness
keyhole_size = config.switch_hole_size
keyswitch_height = config.switch_height
keyswitch_width = config.switch_width
plate_outer_width = keyhole_size + switch_rim_thickness * 2

max_num_rows = config.max_rows
num_cols = config.num_cols
num_pinky_columns = config.num_pinky_columns
cols_with_max_rows = config.cols_with_max_rows

sa_profile_key_height = config.sa_profile_key_height
sa_length = config.sa_top_length
sa_double_length = config.sa_double_length
total_key_height = switch_thickness + sa_profile_key_height

# 间距配置
extra_height = config.extra_height
extra_width = config.extra_width
mount_height = config.mount_height
mount_width = config.mount_width

tenting_angle = config.tenting_angle
back_tilt_angle = config.back_tilt_angle
z_offset = config.z_offset

# 支撑结构配置
post_width = config.post_width
post_rad = config.post_rad
web_thickness = config.web_thickness

# 底板高度配置
bottom_height = 1.5

should_include_risers = False

def is_pinky_column(col):
    """判断是否为小拇指列"""
    return col >= num_cols - num_pinky_columns

# aka: alpha - 每列的行曲率角度（垂直方向曲率）
def row_curve_angle_for_column(col):
    """确定每列的行曲率角度（垂直方向曲率）"""
    if col == 1:  # 食指列
        return 20  # 增加弯曲度
    elif col >= num_cols - num_pinky_columns:  # 小拇指列
        return 22  # 增加弯曲度
    else:
        return 17  # 保持其他列不变

# aka: beta - 列曲率角度（水平方向曲率）
col_curve_angle = 4.0

# 列曲率半径（水平方向曲率）
column_curvature_radius = total_key_height + ((mount_width + extra_width) / 2) / sin(radians(col_curve_angle) / 2)

def row_curvature_radius(col):
    """计算每列的行曲率半径（垂直方向曲率）"""
    return total_key_height + ((mount_height + extra_height) / 2) / sin(radians(row_curve_angle_for_column(col)) / 2)

# 曲率参考中心（水平和垂直方向的曲率参考点）
center_col = 3  # 中心列（从0开始，通常是无名指列）
center_row = 1  # 中心行（从0开始，通常是主行）

def column_extra_transform(col):
    """为特定列应用额外的变换"""
    if is_pinky_column(col):
        return compose(
            rotate_x(6),
            rotate_y(-3)
        )
    else:
        return identity()

def num_rows_for_col(col):
    """确定每列的行数"""
    if col in cols_with_max_rows:
        return max_num_rows
    else:
        return max_num_rows - 1

def does_coord_exist(row, col):
    """检查坐标是否存在于键盘网格中"""
    return col >= 0 and col < num_cols and row >= 0 and row < num_rows_for_col(col)

def negative(vect):
    """返回向量的负值"""
    return [-x for x in vect]

def bottom_transform(height):
    """底部变换函数"""
    return extrude_linear(height)(project())

def bottom_hull(shape):
    """底部外壳构造函数"""
    return hull(shape, bottom_transform(0.1)(shape))

def column_offset(col):
    """计算列的偏移量 [x, y, z]
    - x: 正值向右偏移，负值向左偏移
    - y: 正值向远离使用者方向偏移，负值向靠近使用者方向偏移
    - z: 正值向上抬高，负值向下降低
    """
    if col == 2:  # 中指列
        return [0, 7, -3]  # 向后偏移，略降低
    elif col == 3:  # 无名指列
        return [0, 3, -1.5]  # 向后偏移，略降低
    elif is_pinky_column(col):  # 小拇指列
        return [1.0, -12.5, 5.0]  # 向右偏移，大幅向前，抬高
    else:  # 大拇指和食指列
        return [0, 0, 0]  # 无偏移

def column_z_rotation(col):
    """计算列的Z轴旋转角度（主要用于小拇指区域）"""
    if is_pinky_column(col):
        return -3.0
    else:
        return 0

def place_on_grid_base(row, column, domain):
    """计算给定行列位置的变换矩阵"""
    column_angle = col_curve_angle * (center_col - column)
    row_angle = row_curve_angle_for_column(column) * (center_row - row)

    # 使用矩阵乘法组合所有变换
    transforms = [
        # 垂直方向曲率（X轴旋转）- 先上移到曲率中心，旋转，再下移回原位
        domain.translate(0, 0, -row_curvature_radius(column)),
        domain.rotate_x(row_angle),
        domain.translate(0, 0, row_curvature_radius(column)),
        
        # 水平方向曲率（Y轴旋转）- 先上移到曲率中心，旋转，再下移回原位
        domain.translate(0, 0, -column_curvature_radius),
        domain.rotate_y(column_angle),
        domain.translate(0, 0, column_curvature_radius),

        # Z轴旋转调整（主要用于小拇指区域）
        domain.rotate_z(column_z_rotation(column)),

        # 列位置偏移调整（调整不同列的位置和高度）
        domain.translate(*column_offset(column)),
        
        # 整体键盘调整
        domain.rotate_y(tenting_angle),  # 左右倾斜（绕Y轴）
        domain.rotate_x(back_tilt_angle),  # 整体后倾（绕X轴）
        domain.translate(0, 0, z_offset),  # 基础高度调整
    ]
    
    return domain.compose(*transforms)

def place_on_grid(row, column):
    """放置物体到网格位置"""
    return place_on_grid_base(row, column, lib)

def point_on_grid(row, column, x, y, z):
    """计算给定行列位置的点的最终位置"""
    point = mat.point3(x, y, z)
    tx_point = place_on_grid_base(row, column, mat) @ point
    return mat.to_point(tx_point)

def grid_position(row, col, shape):
    """将形状定位到网格上的特定位置"""
    return place_on_grid(row, col)(shape)

def row_cols():
    """迭代所有有效的行列组合"""
    for row in range(max_num_rows):
        for col in range(num_cols):
            if row < num_rows_for_col(col):
                yield (row, col)

def all_of_shape(shape):
    """在所有有效位置放置形状"""
    return [grid_position(row, col, shape) for (row, col) in row_cols()]

def blocker():
    """创建一个用于减去部分的大块"""
    size = 500
    shape = cube(size, size, size)
    shape = translate(-size/2, -size/2, -size)(shape)
    return shape