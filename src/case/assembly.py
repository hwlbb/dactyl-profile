"""
键盘组装 - 将所有组件组合成最终的键盘模型
"""
from ..lib import *
from ..keyboard_utils import should_include_risers, blocker
from ..switches import all_switches, filled_switches
from ..supports import connectors
from .walls import case_walls
from .reset_switch import reset_switch_body
from .fasteners import screw_insert_all_shapes, screw_insert_outer, screw_insert_inner
from .connectors import trrs_holder, trrs_holder_hole, usb_holder_rim, usb_holder_hole
from .bottom_plate import bottom_plate

def right_shell():
    """创建右侧键盘外壳"""
    global should_include_risers
    should_include_risers = True
    
    from ..thumb_cluster import (
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

def left_bottom_plate():
    """创建左侧键盘底板"""
    return flip_lr()(bottom_plate())
