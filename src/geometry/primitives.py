"""
基础几何形状 - 提供参数化的基础几何形状

该模块包装了基础的几何形状（如立方体、球体、圆柱体等）并提供了一致的接口。
所有形状都以字典格式描述，便于序列化和在不同语言间传递。
"""
from typing import Dict, Any, List, Union, Optional
import solid


def create_cube(size: Union[float, List[float]], center: bool = False) -> Dict[str, Any]:
    """
    创建立方体描述
    
    Args:
        size: 尺寸，可以是单一数值或[x, y, z]列表
        center: 是否居中
        
    Returns:
        形状描述字典
    """
    if isinstance(size, (int, float)):
        size = [size, size, size]
    
    return {
        'type': 'cube',
        'params': {
            'size': size,
            'center': center
        }
    }


def create_sphere(radius: float, segments: int = 30) -> Dict[str, Any]:
    """
    创建球体描述
    
    Args:
        radius: 半径
        segments: 细分段数
        
    Returns:
        形状描述字典
    """
    return {
        'type': 'sphere',
        'params': {
            'radius': radius,
            'segments': segments
        }
    }


def create_cylinder(
    height: float,
    radius: Optional[float] = None,
    radius1: Optional[float] = None,
    radius2: Optional[float] = None,
    segments: int = 30,
    center: bool = False
) -> Dict[str, Any]:
    """
    创建圆柱体或圆台描述
    
    Args:
        height: 高度
        radius: 半径（如果是均匀圆柱体）
        radius1: 底部半径（如果是圆台）
        radius2: 顶部半径（如果是圆台）
        segments: 细分段数
        center: 是否居中
        
    Returns:
        形状描述字典
    """
    params = {
        'height': height,
        'segments': segments,
        'center': center
    }
    
    if radius is not None:
        params['radius'] = radius
    else:
        if radius1 is not None:
            params['radius1'] = radius1
        if radius2 is not None:
            params['radius2'] = radius2
    
    return {
        'type': 'cylinder',
        'params': params
    }


def create_square(size: Union[float, List[float]], center: bool = False) -> Dict[str, Any]:
    """
    创建正方形或矩形描述
    
    Args:
        size: 尺寸，可以是单一数值或[x, y]列表
        center: 是否居中
        
    Returns:
        形状描述字典
    """
    if isinstance(size, (int, float)):
        size = [size, size]
    
    return {
        'type': 'square',
        'params': {
            'size': size,
            'center': center
        }
    }


def shape_to_solid(shape_data: Dict[str, Any]):
    """
    将形状描述转换为solid对象
    
    Args:
        shape_data: 形状描述字典
        
    Returns:
        对应的solid对象
    """
    shape_type = shape_data['type']
    params = shape_data['params']
    
    if shape_type == 'cube':
        return solid.cube(params['size'], center=params.get('center', False))
    
    elif shape_type == 'sphere':
        return solid.sphere(r=params['radius'], segments=params.get('segments', 30))
    
    elif shape_type == 'cylinder':
        if 'radius' in params:
            return solid.cylinder(
                h=params['height'],
                r=params['radius'],
                segments=params.get('segments', 30),
                center=params.get('center', False)
            )
        else:
            return solid.cylinder(
                h=params['height'],
                r1=params.get('radius1', 1),
                r2=params.get('radius2', 1),
                segments=params.get('segments', 30),
                center=params.get('center', False)
            )
    
    elif shape_type == 'square':
        return solid.square(params['size'], center=params.get('center', False))
    
    else:
        raise ValueError(f"未知的形状类型: {shape_type}")
