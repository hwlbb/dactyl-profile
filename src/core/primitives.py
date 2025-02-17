from typing import List, Union, Tuple
from .shape import Shape

def cube(size: Union[float, List[float], Tuple[float, float, float]], center: bool = False) -> Shape:
    """创建立方体
    
    Args:
        size: 如果是单个数字，表示所有边长相等；如果是列表/元组，表示[x, y, z]三个方向的边长
        center: 是否居中，默认为False（从原点开始）
    """
    if isinstance(size, (int, float)):
        size = [float(size), float(size), float(size)]
    return Shape('cube', {
        'size': size,
        'center': center
    })

def sphere(radius: float, segments: int = 30) -> Shape:
    """创建球体
    
    Args:
        radius: 半径
        segments: 分段数，影响渲染精度，默认30
    """
    return Shape('sphere', {
        'radius': float(radius),
        'segments': segments
    })

def cylinder(radius: float, height: float, segments: int = 30) -> Shape:
    """创建圆柱体
    
    Args:
        radius: 底面圆的半径
        height: 高度
        segments: 分段数，影响渲染精度，默认30
    """
    return Shape('cylinder', {
        'radius': float(radius),
        'height': float(height),
        'segments': segments
    }) 