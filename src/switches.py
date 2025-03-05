"""
开关和键帽 - 处理机械键盘开关和键帽相关的函数
"""
from .lib import *
from .shapes import *
from .keyboard_utils import (
    switch_thickness, switch_rim_thickness, keyhole_size, 
    plate_outer_width, sa_length, sa_profile_key_height
)

def single_switch_fn():
    """创建单个开关的形状"""
    outer_width = keyhole_size + switch_rim_thickness * 2

    bottom_wall = cube(outer_width, switch_rim_thickness, switch_thickness)
    top_wall = translate(0, keyhole_size + switch_rim_thickness, 0)(bottom_wall)

    left_wall = cube(switch_rim_thickness, outer_width, switch_thickness)
    right_wall = translate(keyhole_size + switch_rim_thickness, 0, 0)(left_wall)

    nub_len = 2.75
    nub_cyl = translate(0, 0, -1)(rotate_x(90)(cylinder(1, nub_len, 30, center=True)))
    nub_cube = translate(-switch_rim_thickness / 2, 0, 0.)(cube(switch_rim_thickness, nub_len, 4, center=True))
    left_nub = translate(switch_rim_thickness, (outer_width) / 2, 0)(hull(nub_cyl, nub_cube))

    right_nub_cube = translate(switch_rim_thickness / 2, 0, 0)(cube(switch_rim_thickness, nub_len, 4, center=True))
    right_nub = translate(-switch_rim_thickness + outer_width, (outer_width) / 2, 0)(hull(nub_cyl, right_nub_cube))

    return translate(-outer_width/2, -outer_width/2, 0)(union(
            bottom_wall,
            top_wall,
            left_wall,
            right_wall,
            left_nub,
            right_nub,
            ))

# 创建单个开关形状
single_switch = single_switch_fn()

# 创建填充开关形状 (没有中间开孔)
filled_switch = translate(0, 0, switch_thickness / 2.0)(cube(plate_outer_width, plate_outer_width, switch_thickness, center=True))

def sa_cap_fn():
    """创建SA键帽的形状"""
    m = 17.0

    bot = square(sa_length, sa_length, center=True)
    bot = extrude_linear(0.1)(bot)

    mid = square(m, m, center=True)
    mid = extrude_linear(0.1)(mid)
    mid = translate(0, 0, 6)(mid)

    top = square(12, 12, center=True)
    top = extrude_linear(0.1)(top)
    top = translate(0, 0, 12)(top)

    return colour(220, 163, 163, 1)(translate(0, 0, 5 + switch_thickness)(hull(bot, mid, top)))

# 创建SA键帽形状
sa_cap = sa_cap_fn()

# 添加在所有位置创建开关和键帽的函数
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