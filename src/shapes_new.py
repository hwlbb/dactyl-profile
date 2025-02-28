"""
shapes_new.py - 使用重新设计的lib库实现基本形状
测试lib_redesign的兼容性和功能
"""
from .lib_redesign import *
from math import radians, sin, cos

SWITCH_RISER_RADIUS = 0.8
SWITCH_RISER_HEIGHT = 9.0


def switch_riser_raw_dot_fn():
    """创建开关支架的基础点"""
    return sphere(SWITCH_RISER_RADIUS)


switch_riser_raw_dot = switch_riser_raw_dot_fn()

top_dot = translate(0, 0, SWITCH_RISER_HEIGHT)(switch_riser_raw_dot)

def switch_riser_post_fn():
    """创建开关支架柱"""
    post = translate(0, 0, SWITCH_RISER_HEIGHT / 2)(
        cylinder(SWITCH_RISER_RADIUS, SWITCH_RISER_HEIGHT, center=True)
    )

    return union(post, top_dot)


switch_riser_post = switch_riser_post_fn()
