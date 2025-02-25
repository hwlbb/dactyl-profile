"""
拇指区域 - 处理键盘拇指区域的相关功能
"""
from .lib import *
from .shapes import *
from .keyboard_utils import (
    point_on_grid, num_rows_for_col, should_include_risers, 
    bottom_hull
)
from .switches import single_switch, filled_switch, sa_cap
from .supports import (
    web_post, web_post_br, switch_riser_post, switch_riser_raw_dot,
    square_idx_tl, square_idx_tr, square_idx_bl, square_idx_br,
    switch_riser_offset_square, get_in_square, top_dot,
    web_posts, make_offsetter, web_post_tr, web_post_tl, web_post_bl
)

# 拇指区域的基础位置
thumb_basic_postition = point_on_grid(num_rows_for_col(1), 1, 0, 0, 0)
thumb_offsets = [15, 7, -5]
thumb_position = [sum(x) for x in zip(thumb_basic_postition, thumb_offsets)]

def thumb_placer(rot, move):
    """创建拇指区域的定位函数"""
    return compose(
        rotate_x(rot[0]),
        rotate_y(rot[1]),
        rotate_z(rot[2]),
        translate(*move),
        rotate_z(-10),
        translate(*thumb_position),
    )

# 拇指区域各个键的定位器
thumb_r_placer = thumb_placer([14, -40, 12], [-15.4, -9.8, 5.2])
thumb_m_placer = thumb_placer([10, -23, 20], [-33, -15, -6])
thumb_l_placer = thumb_placer([6, -5, 35], [-52.8, -25.5, -11.5])
thumb_bl_placer = thumb_placer([4, -10, 27], [-33.3, -36.2, -16])
thumb_br_placer = thumb_placer([4, -26, 18], [-13.8, -28.7, -9.6])

thumb_placement_fns = [
    thumb_r_placer,
    thumb_m_placer,
    thumb_l_placer,
    thumb_br_placer,
    thumb_bl_placer,
]

def thumbs_post_offsets(placer, post):
    """获取拇指区域支柱的偏移量"""
    if placer == thumb_br_placer:
        if post == square_idx_bl:
            return [3, 0, 0]
        if post == square_idx_tr:
            return [0, -3.8, 0]

    if placer == thumb_r_placer:
        if post == square_idx_bl:
            return [11, 0, 0]
        if post == square_idx_tl:
            return [4, 0, 0]

    if placer == thumb_bl_placer:
        if post == square_idx_br:
            return [-3, 0, 0]
        if post == square_idx_tl:
            return [0, -3, 0]

    if placer == thumb_l_placer:
        if post == square_idx_br:
            return [-11.5, 0, 0]

    if placer == thumb_m_placer:
        if post == square_idx_tr:
            return [-2, 0, 0]

    return None

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
    """连接两个拇指区域位置的墙壁"""
    offsetter1 = make_offsetter(idx1, delta1)
    offsetter2 = make_offsetter(idx2, delta2)

    post1 = offsetter1(switch_riser_post)
    post2 = offsetter2(switch_riser_post)

    shapes = []

    # 使用参数include_risers来控制是否添加上边框
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

def thumb_wall(place_fn1, idx1, place_fn2, idx2, **kwargs):
    """创建拇指区域的墙壁"""
    d1 = thumbs_post_offsets(place_fn1, idx1)
    d2 = thumbs_post_offsets(place_fn2, idx2)

    return wall_connect_from_placer(place_fn1, idx1, place_fn2, idx2, delta1=d1, delta2=d2, **kwargs)

def get_offset_thumb_placer(placer, idx, shape):
    """获取带偏移的拇指区域定位器"""
    delta = thumbs_post_offsets(placer, idx)
    return placer(make_offsetter(idx, delta)(shape))

def thumb_walls():
    """创建拇指区域的墙壁"""
    return union(
        thumb_wall(thumb_bl_placer, square_idx_bl, thumb_bl_placer, square_idx_br, include_risers=True),
        thumb_wall(thumb_bl_placer, square_idx_br, thumb_br_placer, square_idx_bl, include_risers=True),
        thumb_wall(thumb_br_placer, square_idx_bl, thumb_br_placer, square_idx_br, include_risers=True),

        thumb_wall(thumb_bl_placer, square_idx_bl, thumb_bl_placer, square_idx_tl, include_risers=True),

        thumb_wall(thumb_bl_placer, square_idx_tl, thumb_l_placer, square_idx_br, connectors=False, include_risers=True),
        thumb_wall(thumb_l_placer, square_idx_br, thumb_l_placer, square_idx_bl, connectors=False, include_risers=True),

        thumb_wall(thumb_l_placer, square_idx_bl, thumb_l_placer, square_idx_tl, include_risers=True),
        thumb_wall(thumb_l_placer, square_idx_tl, thumb_l_placer, square_idx_tr, include_risers=True),

        thumb_wall(thumb_l_placer, square_idx_tr, thumb_m_placer, square_idx_tl, include_risers=True),
        thumb_wall(thumb_m_placer, square_idx_tl, thumb_m_placer, square_idx_tr, walls=False, include_risers=True),

        thumb_wall(thumb_m_placer, square_idx_tr, thumb_r_placer, square_idx_tl, walls=False, include_risers=True),
        thumb_wall(thumb_r_placer, square_idx_tl, thumb_r_placer, square_idx_tr, walls=False, include_risers=True),

        thumb_wall(thumb_r_placer, square_idx_tr, thumb_r_placer, square_idx_br, walls=False, include_risers=True),

        thumb_wall(thumb_br_placer, square_idx_br, thumb_br_placer, square_idx_tr, include_risers=True),

        thumb_wall(thumb_r_placer, square_idx_bl, thumb_r_placer, square_idx_br, walls=False, connectors=False, include_risers=True),

        hull(
            get_offset_thumb_placer(thumb_br_placer, square_idx_tr, top_dot),
            get_offset_thumb_placer(thumb_r_placer, square_idx_bl, top_dot),
            get_offset_thumb_placer(thumb_r_placer, square_idx_bl, switch_riser_raw_dot),
        ),

        hull(
            get_offset_thumb_placer(thumb_br_placer, square_idx_tr, top_dot),
            get_offset_thumb_placer(thumb_br_placer, square_idx_tr, switch_riser_raw_dot),
            get_offset_thumb_placer(thumb_r_placer, square_idx_bl, switch_riser_raw_dot),
        ),

        hull(
            get_offset_thumb_placer(thumb_r_placer, square_idx_br, switch_riser_raw_dot),
            get_offset_thumb_placer(thumb_r_placer, square_idx_bl, switch_riser_raw_dot),
            get_offset_thumb_placer(thumb_br_placer, square_idx_tr, switch_riser_raw_dot),
        ),

        bottom_hull(
            hull(
                get_offset_thumb_placer(thumb_r_placer, square_idx_br, switch_riser_raw_dot),
                get_offset_thumb_placer(thumb_br_placer, square_idx_tr, switch_riser_raw_dot),
            )
        ),
    )

def thumb_connectors():
    """创建拇指区域的连接结构"""
    right_thumb_cover_sphere = get_offset_thumb_placer(thumb_r_placer, square_idx_bl, translate(0, 1.7, 0)(web_post))

    left_thumb_cover_lower_sphere = get_offset_thumb_placer(thumb_bl_placer, square_idx_tl, translate(0, 2, 0)(web_post))
    left_thumb_cover_upper_sphere = thumb_l_placer(translate(0, 0, 0)(web_post_br))

    br_tr_with_offset = thumb_br_placer(translate(0.8, 0.2, 0)(web_post_tr))

    thumb_l_special_point = get_offset_thumb_placer(thumb_l_placer, square_idx_bl, translate(10, 1.1, 0)(web_post))

    return union(
        # 中间和右侧拇指键连接
        hull(
            thumb_m_placer(web_post_tr),
            thumb_m_placer(web_post_br),
            thumb_r_placer(web_post_tl),
            thumb_r_placer(web_post_bl),
        ),
        # 中间和左侧拇指键连接
        hull(
            thumb_m_placer(web_post_tl),
            thumb_l_placer(web_post_tr),
            thumb_m_placer(web_post_bl),
            thumb_l_placer(web_post_br),
            thumb_m_placer(web_post_bl),
        ),
        hull(
            thumb_bl_placer(web_post_tr),
            thumb_bl_placer(web_post_br),
            thumb_br_placer(web_post_tl),
            thumb_br_placer(web_post_bl),
        ),
        # 其他连接器(共9个)
        hull(
            thumb_bl_placer(web_post_tl),
            thumb_m_placer(web_post_bl),
            thumb_l_placer(web_post_br),
        ),
        hull(
            thumb_bl_placer(web_post_tl),
            thumb_bl_placer(web_post_tr),
            thumb_m_placer(web_post_bl),
        ),
        hull(
            thumb_bl_placer(web_post_tr),
            thumb_m_placer(web_post_bl),
            thumb_m_placer(web_post_br),
        ),
        hull(
            thumb_br_placer(web_post_tl),
            thumb_bl_placer(web_post_tr),
            thumb_m_placer(web_post_br)
        ),
        hull(
            thumb_m_placer(web_post_br),
            thumb_r_placer(web_post_bl),
            thumb_br_placer(web_post_tl),
        ),
        hull(
            thumb_r_placer(web_post_bl),
            thumb_br_placer(web_post_tl),
            br_tr_with_offset,
        ),
        hull(
            thumb_r_placer(web_post_bl),
            thumb_r_placer(web_post_br),
            br_tr_with_offset,
        ),

        # 右侧特殊连接器
        hull(
            right_thumb_cover_sphere,
            get_offset_thumb_placer(thumb_r_placer, square_idx_bl, web_post),
            thumb_r_placer(web_post_br),
            get_offset_thumb_placer(thumb_r_placer, square_idx_br, web_post),
        ),
        hull(
            right_thumb_cover_sphere,
            get_offset_thumb_placer(thumb_r_placer, square_idx_bl, web_post),
            get_offset_thumb_placer(thumb_br_placer, square_idx_tr, switch_riser_raw_dot),
            br_tr_with_offset,
        ),

        # 左侧特殊连接器
        hull(
            thumb_l_placer(web_post_bl),
            get_offset_thumb_placer(thumb_l_placer, square_idx_bl, web_post),
            thumb_l_special_point,
        ),
        hull(
            thumb_l_placer(web_post_bl),
            thumb_l_placer(web_post_br),
            thumb_l_special_point,
        ),
        hull(
            left_thumb_cover_lower_sphere,
            get_offset_thumb_placer(thumb_bl_placer, square_idx_tl, web_post),
            thumb_bl_placer(web_post_tl),
        ),
        hull(
            left_thumb_cover_lower_sphere,
            thumb_bl_placer(web_post_tl),
            left_thumb_cover_upper_sphere,
        ),
        hull(
            left_thumb_cover_lower_sphere,
            left_thumb_cover_upper_sphere,
            thumb_l_special_point,
        ),
        hull(
            left_thumb_cover_lower_sphere,
            get_offset_thumb_placer(thumb_l_placer, square_idx_br, web_post),
            thumb_l_special_point,
            get_offset_thumb_placer(thumb_bl_placer, square_idx_tl, web_post),
        ),
    )

def thumb_to_body_connectors():
    """创建拇指区域到主键盘的连接结构"""
    from .keyboard_utils import place_on_grid
    
    return union(
        # 右侧拇指键到主键盘的连接
        bottom_hull(
            hull(
                thumb_r_placer(get_in_square(switch_riser_offset_square, square_idx_br)(switch_riser_raw_dot)),
                place_on_grid(3, 2)(get_in_square(switch_riser_offset_square, square_idx_bl)(switch_riser_raw_dot)),
            )
        ),
        hull(
            thumb_r_placer(get_in_square(switch_riser_offset_square, square_idx_br)(switch_riser_raw_dot)),
            thumb_r_placer(get_in_square(switch_riser_offset_square, square_idx_tr)(switch_riser_raw_dot)),
            place_on_grid(3, 2)(get_in_square(switch_riser_offset_square, square_idx_bl)(switch_riser_raw_dot)),
        ),
        hull(
            thumb_r_placer(get_in_square(switch_riser_offset_square, square_idx_tr)(switch_riser_raw_dot)),
            place_on_grid(3, 2)(get_in_square(switch_riser_offset_square, square_idx_bl)(switch_riser_raw_dot)),
            place_on_grid(2, 1)(get_in_square(switch_riser_offset_square, square_idx_br)(switch_riser_raw_dot)),
        ),
        hull(
            thumb_r_placer(get_in_square(switch_riser_offset_square, square_idx_tr)(switch_riser_raw_dot)),
            thumb_r_placer(get_in_square(switch_riser_offset_square, square_idx_tl)(switch_riser_raw_dot)),
            place_on_grid(2, 1)(get_in_square(switch_riser_offset_square, square_idx_br)(switch_riser_raw_dot)),
        ),

        # 中间拇指键到主键盘的连接
        bottom_hull(
            hull(
                thumb_m_placer(get_in_square(switch_riser_offset_square, square_idx_tl)(switch_riser_raw_dot)),
                place_on_grid(2, 0)(get_in_square(switch_riser_offset_square, square_idx_bl)(switch_riser_raw_dot)),
            )
        ),
        hull(
            thumb_m_placer(get_in_square(switch_riser_offset_square, square_idx_tl)(switch_riser_raw_dot)),
            place_on_grid(2, 0)(get_in_square(switch_riser_offset_square, square_idx_bl)(switch_riser_raw_dot)),
            place_on_grid(2, 0)(get_in_square(switch_riser_offset_square, square_idx_br)(switch_riser_raw_dot)),
        ),
    )

def thumb_switches():
    """创建拇指区域所有开关"""
    return union(*[fn(single_switch) for fn in thumb_placement_fns])

def filled_thumb_switches():
    """创建拇指区域所有填充开关(没有开孔)"""
    return union(*[fn(filled_switch) for fn in thumb_placement_fns])

def bottom_edge_at_position(row, col):
    """获取底部边缘的位置"""
    yield row, col, square_idx_bl
    yield row, col, square_idx_br

def bottom_edge_iterator():
    """迭代底部边缘的所有位置"""
    from .keyboard_utils import num_cols, num_rows_for_col
    
    for col in range(num_cols):
        row = num_rows_for_col(col) - 1
        yield from bottom_edge_at_position(row, col)
    return

def thumb_spots():
    """返回拇指区域的关键点"""
    return [
        [thumb_l_placer, square_idx_tl],
        [thumb_l_placer, square_idx_tr],
        [thumb_m_placer, square_idx_tl],
        [thumb_m_placer, square_idx_tr],
        [thumb_r_placer, square_idx_tl],
        [thumb_r_placer, square_idx_tr],
        [thumb_r_placer, square_idx_br],
        [thumb_br_placer, square_idx_br],
    ]

def thumb_caps():
    """创建拇指区域的键帽"""
    return union(*[fn(sa_cap) for fn in thumb_placement_fns[-2:]])

def thumb_corner():
    """创建拇指区角落的测试部分"""
    global should_include_risers
    should_include_risers = True
    
    from .keyboard_utils import blocker
    
    return difference(
        union(
            thumb_switches(),
            thumb_walls(),
            thumb_connectors(),
            # thumb_caps(),
            thumb_to_body_connectors(),
        ),
        union(
            blocker(),
        ))