"""
几何系统 - 提供基础形状和操作
"""
from typing import Dict, Any, Union, Optional
from ..core.scene import Node, Scene, GeometryNode, OperationNode, TransformNode

def create_node_from_shape(shape_data: Dict[str, Any], scene: Optional[Scene] = None, name: Optional[str] = None) -> Node:
    """
    从形状描述创建场景节点
    
    Args:
        shape_data: 形状或操作描述
        scene: 可选的场景
        name: 节点名称
        
    Returns:
        创建的节点
    """
    if 'type' in shape_data:
        # 基本几何体
        node = GeometryNode(shape_data, name=name)
    elif 'op' in shape_data:
        # 操作
        op_type = shape_data['op']
        
        # 处理根据操作类型创建不同的节点
        if op_type in ['union', 'intersection', 'hull']:
            # 布尔操作
            node = OperationNode(op_type, name=name)
            
            # 添加子节点
            for i, shape in enumerate(shape_data['shapes']):
                child = create_node_from_shape(shape, name=f"{name}_{i}" if name else None)
                node.add(child)
                
        elif op_type == 'difference':
            # 差集操作
            node = OperationNode(op_type, name=name)
            
            # 添加主形状作为子节点
            main_node = create_node_from_shape(shape_data['shape'], name=f"{name}_main" if name else None)
            node.add(main_node)
            
            # 添加工具形状作为子节点
            for i, tool in enumerate(shape_data['tools']):
                tool_node = create_node_from_shape(tool, name=f"{name}_tool_{i}" if name else None)
                node.add(tool_node)
                
        elif op_type == 'translate':
            # 创建转换数据
            transform_data = {
                'type': 'translate',
                'args': shape_data['args']
            }
            
            # 创建转换节点
            node = TransformNode(transform_data, name=name)
            
            # 添加被转换的形状
            child_node = create_node_from_shape(shape_data['shape'], name=f"{name}_shape" if name else None)
            node.add(child_node)
            
        elif op_type == 'rotate':
            # 创建转换数据
            transform_data = {
                'type': 'rotate',
                'angle': shape_data['angle'],
                'axis': shape_data['axis']
            }
            
            # 创建转换节点
            node = TransformNode(transform_data, name=name)
            
            # 添加被转换的形状
            child_node = create_node_from_shape(shape_data['shape'], name=f"{name}_shape" if name else None)
            node.add(child_node)
            
        elif op_type == 'scale':
            # 创建转换数据
            transform_data = {
                'type': 'scale',
                'args': shape_data['args']
            }
            
            # 创建转换节点
            node = TransformNode(transform_data, name=name)
            
            # 添加被转换的形状
            child_node = create_node_from_shape(shape_data['shape'], name=f"{name}_shape" if name else None)
            node.add(child_node)
            
        elif op_type == 'projection':
            # 创建转换数据
            transform_data = {
                'type': 'projection',
                'cut': shape_data.get('cut', False)
            }
            
            # 创建转换节点
            node = TransformNode(transform_data, name=name)
            
            # 添加被转换的形状
            child_node = create_node_from_shape(shape_data['shape'], name=f"{name}_shape" if name else None)
            node.add(child_node)
            
        elif op_type == 'extrude_linear':
            # 创建转换数据
            transform_data = {
                'type': 'extrude_linear',
                'height': shape_data['height']
            }
            
            # 创建转换节点
            node = TransformNode(transform_data, name=name)
            
            # 添加被转换的形状
            child_node = create_node_from_shape(shape_data['shape'], name=f"{name}_shape" if name else None)
            node.add(child_node)
            
        else:
            # 其他未知操作
            raise ValueError(f"未知的操作类型: {op_type}")
    else:
        raise ValueError(f"无法识别的形状描述: {shape_data}")
    
    # 如果提供了场景，将节点添加到场景
    if scene is not None:
        scene.add(node)
    
    return node
