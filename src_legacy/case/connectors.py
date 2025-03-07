"""
接口系统 - 处理TRRS和USB连接器
"""
from ..lib import *
from ..keyboard_utils import point_on_grid, keyswitch_width

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
