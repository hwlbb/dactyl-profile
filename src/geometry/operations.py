"""
几何操作 - 提供布尔操作和其他几何变换

该模块包装了基础的布尔操作（如并集、差集、凸包等）和其他几何变换，
提供统一的接口和数据格式。
"""
from typing import Dict, Any, List, Union, Optional
import solid
from .primitives import shape_to_solid


def create_union(shapes: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    创建并集操作描述
    
    Args:
        shapes: 要进行并集操作的形状列表
        
    Returns:
        操作描述字典
    """
    return {
        'op': 'union',
        'shapes': shapes
    }


def create_difference(shape: Dict[str, Any], tools: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    创建差集操作描述
    
    Args:
        shape: 主形状
        tools: 要减去的形状列表
        
    Returns:
        操作描述字典
    """
    return {
        'op': 'difference',
        'shape': shape,
        'tools': tools
    }


def create_intersection(shapes: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    创建交集操作描述
    
    Args:
        shapes: 要进行交集操作的形状列表
        
    Returns:
        操作描述字典
    """
    return {
        'op': 'intersection',
        'shapes': shapes
    }


def create_hull(shapes: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    创建凸包操作描述
    
    Args:
        shapes: 要进行凸包操作的形状列表
        
    Returns:
        操作描述字典
    """
    return {
        'op': 'hull',
        'shapes': shapes
    }


def create_projection(shape: Dict[str, Any], cut: bool = False) -> Dict[str, Any]:
    """
    创建投影操作描述
    
    Args:
        shape: 要投影的形状
        cut: 是否进行截面投影
        
    Returns:
        操作描述字典
    """
    return {
        'op': 'projection',
        'shape': shape,
        'cut': cut
    }


def create_extrude_linear(shape: Dict[str, Any], height: float) -> Dict[str, Any]:
    """
    创建线性拉伸操作描述
    
    Args:
        shape: 要拉伸的2D形状
        height: 拉伸高度
        
    Returns:
        操作描述字典
    """
    return {
        'op': 'extrude_linear',
        'shape': shape,
        'height': height
    }


def create_translate(shape: Dict[str, Any], x: float, y: float, z: float) -> Dict[str, Any]:
    """
    创建平移操作描述
    
    Args:
        shape: 要平移的形状
        x: X轴平移量
        y: Y轴平移量
        z: Z轴平移量
        
    Returns:
        操作描述字典
    """
    return {
        'op': 'translate',
        'shape': shape,
        'args': [x, y, z]
    }


def create_rotate(shape: Dict[str, Any], angle: float, axis: List[float]) -> Dict[str, Any]:
    """
    创建旋转操作描述
    
    Args:
        shape: 要旋转的形状
        angle: 旋转角度
        axis: 旋转轴[x, y, z]
        
    Returns:
        操作描述字典
    """
    return {
        'op': 'rotate',
        'shape': shape,
        'angle': angle,
        'axis': axis
    }


def create_scale(shape: Dict[str, Any], x: float, y: float, z: float) -> Dict[str, Any]:
    """
    创建缩放操作描述
    
    Args:
        shape: 要缩放的形状
        x: X轴缩放比例
        y: Y轴缩放比例
        z: Z轴缩放比例
        
    Returns:
        操作描述字典
    """
    return {
        'op': 'scale',
        'shape': shape,
        'args': [x, y, z]
    }


def operation_to_solid(op_data: Dict[str, Any]):
    """
    将操作描述转换为solid对象
    
    Args:
        op_data: 操作描述字典
        
    Returns:
        对应的solid对象
    """
    op_type = op_data['op']
    
    if op_type == 'union':
        shapes = [shape_to_solid(s) if 'type' in s else operation_to_solid(s) for s in op_data['shapes']]
        return solid.union()(*shapes)
    
    elif op_type == 'difference':
        shape = shape_to_solid(op_data['shape']) if 'type' in op_data['shape'] else operation_to_solid(op_data['shape'])
        tools = [shape_to_solid(t) if 'type' in t else operation_to_solid(t) for t in op_data['tools']]
        return solid.difference()(shape, *tools)
    
    elif op_type == 'intersection':
        shapes = [shape_to_solid(s) if 'type' in s else operation_to_solid(s) for s in op_data['shapes']]
        return solid.intersection()(*shapes)
    
    elif op_type == 'hull':
        shapes = [shape_to_solid(s) if 'type' in s else operation_to_solid(s) for s in op_data['shapes']]
        return solid.hull()(*shapes)
    
    elif op_type == 'projection':
        shape = shape_to_solid(op_data['shape']) if 'type' in op_data['shape'] else operation_to_solid(op_data['shape'])
        return solid.projection(cut=op_data['cut'])(shape)
    
    elif op_type == 'extrude_linear':
        shape = shape_to_solid(op_data['shape']) if 'type' in op_data['shape'] else operation_to_solid(op_data['shape'])
        return solid.linear_extrude(height=op_data['height'])(shape)
    
    elif op_type == 'translate':
        shape = shape_to_solid(op_data['shape']) if 'type' in op_data['shape'] else operation_to_solid(op_data['shape'])
        return solid.translate(op_data['args'])(shape)
    
    elif op_type == 'rotate':
        shape = shape_to_solid(op_data['shape']) if 'type' in op_data['shape'] else operation_to_solid(op_data['shape'])
        return solid.rotate(a=op_data['angle'], v=op_data['axis'])(shape)
    
    elif op_type == 'scale':
        shape = shape_to_solid(op_data['shape']) if 'type' in op_data['shape'] else operation_to_solid(op_data['shape'])
        return solid.scale(op_data['args'])(shape)
    
    else:
        raise ValueError(f"未知的操作类型: {op_type}")
