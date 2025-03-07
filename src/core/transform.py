"""
统一变换系统 - 提供一致的接口进行3D变换

该模块将点变换和对象变换统一在一个接口下，
消除了原有代码中使用两套变换系统的混乱。
"""
import numpy as np
from math import radians, sin, cos
from typing import List, Tuple, Dict, Any, Union, Optional
from .scene import TransformNode, Scene


def create_translation_matrix(x: float, y: float, z: float) -> np.ndarray:
    """
    创建平移矩阵
    
    Args:
        x: X轴平移量
        y: Y轴平移量
        z: Z轴平移量
        
    Returns:
        4x4平移矩阵
    """
    return np.array([
        [1, 0, 0, x],
        [0, 1, 0, y],
        [0, 0, 1, z],
        [0, 0, 0, 1]
    ])


def create_rotation_x_matrix(angle_deg: float) -> np.ndarray:
    """
    创建绕X轴旋转矩阵
    
    Args:
        angle_deg: 旋转角度(度)
        
    Returns:
        4x4旋转矩阵
    """
    rad = radians(angle_deg)
    return np.array([
        [1, 0, 0, 0],
        [0, cos(rad), -sin(rad), 0],
        [0, sin(rad), cos(rad), 0],
        [0, 0, 0, 1]
    ])


def create_rotation_y_matrix(angle_deg: float) -> np.ndarray:
    """
    创建绕Y轴旋转矩阵
    
    Args:
        angle_deg: 旋转角度(度)
        
    Returns:
        4x4旋转矩阵
    """
    rad = radians(angle_deg)
    return np.array([
        [cos(rad), 0, sin(rad), 0],
        [0, 1, 0, 0],
        [-sin(rad), 0, cos(rad), 0],
        [0, 0, 0, 1]
    ])


def create_rotation_z_matrix(angle_deg: float) -> np.ndarray:
    """
    创建绕Z轴旋转矩阵
    
    Args:
        angle_deg: 旋转角度(度)
        
    Returns:
        4x4旋转矩阵
    """
    rad = radians(angle_deg)
    return np.array([
        [cos(rad), -sin(rad), 0, 0],
        [sin(rad), cos(rad), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])


def create_scale_matrix(x: float, y: float, z: float) -> np.ndarray:
    """
    创建缩放矩阵
    
    Args:
        x: X轴缩放因子
        y: Y轴缩放因子
        z: Z轴缩放因子
        
    Returns:
        4x4缩放矩阵
    """
    return np.array([
        [x, 0, 0, 0],
        [0, y, 0, 0],
        [0, 0, z, 0],
        [0, 0, 0, 1]
    ])


def identity_matrix() -> np.ndarray:
    """
    创建单位矩阵
    
    Returns:
        4x4单位矩阵
    """
    return np.eye(4)


class TransformSystem:
    """
    统一的变换系统
    
    同时支持点变换和场景节点变换，提供一致的接口。
    """
    
    @staticmethod
    def translate(x: float, y: float, z: float) -> Dict[str, Any]:
        """
        创建平移变换
        
        Args:
            x: X轴平移量
            y: Y轴平移量
            z: Z轴平移量
            
        Returns:
            包含变换信息的字典
        """
        return {
            'type': 'translate',
            'args': [x, y, z],
            'matrix': create_translation_matrix(x, y, z)
        }
    
    @staticmethod
    def rotate_x(angle: float) -> Dict[str, Any]:
        """
        创建绕X轴旋转变换
        
        Args:
            angle: 旋转角度(度)
            
        Returns:
            包含变换信息的字典
        """
        return {
            'type': 'rotate_x',
            'args': [angle],
            'matrix': create_rotation_x_matrix(angle)
        }
    
    @staticmethod
    def rotate_y(angle: float) -> Dict[str, Any]:
        """
        创建绕Y轴旋转变换
        
        Args:
            angle: 旋转角度(度)
            
        Returns:
            包含变换信息的字典
        """
        return {
            'type': 'rotate_y',
            'args': [angle],
            'matrix': create_rotation_y_matrix(angle)
        }
    
    @staticmethod
    def rotate_z(angle: float) -> Dict[str, Any]:
        """
        创建绕Z轴旋转变换
        
        Args:
            angle: 旋转角度(度)
            
        Returns:
            包含变换信息的字典
        """
        return {
            'type': 'rotate_z',
            'args': [angle],
            'matrix': create_rotation_z_matrix(angle)
        }
    
    @staticmethod
    def scale(x: float, y: float, z: float) -> Dict[str, Any]:
        """
        创建缩放变换
        
        Args:
            x: X轴缩放因子
            y: Y轴缩放因子
            z: Z轴缩放因子
            
        Returns:
            包含变换信息的字典
        """
        return {
            'type': 'scale',
            'args': [x, y, z],
            'matrix': create_scale_matrix(x, y, z)
        }
    
    @staticmethod
    def identity() -> Dict[str, Any]:
        """
        创建恒等变换
        
        Returns:
            包含变换信息的字典
        """
        return {
            'type': 'identity',
            'args': [],
            'matrix': identity_matrix()
        }
    
    @staticmethod
    def compose(*transforms) -> Dict[str, Any]:
        """
        组合多个变换
        
        Args:
            transforms: 要组合的变换列表
            
        Returns:
            包含组合变换信息的字典
        """
        if not transforms:
            return TransformSystem.identity()
        
        # 计算组合矩阵
        result_matrix = identity_matrix()
        for transform in transforms:
            result_matrix = transform['matrix'] @ result_matrix
        
        return {
            'type': 'compose',
            'args': [t['args'] for t in transforms],
            'matrix': result_matrix
        }
    
    @staticmethod
    def apply_to_point(transform: Dict[str, Any], point: Union[List[float], np.ndarray]) -> List[float]:
        """
        将变换应用到点
        
        Args:
            transform: 变换信息
            point: 要变换的点 [x, y, z]
            
        Returns:
            变换后的点 [x', y', z']
        """
        # 转换为齐次坐标
        if isinstance(point, list):
            point_array = np.array([point[0], point[1], point[2], 1.0])
        else:
            point_array = np.append(point[:3], 1.0)
        
        # 应用变换
        result = transform['matrix'] @ point_array
        
        # 转回非齐次坐标
        return result[:3].tolist()
    
    @staticmethod
    def create_node(transform: Dict[str, Any], scene: Optional[Scene] = None, name: Optional[str] = None) -> TransformNode:
        """
        从变换创建场景节点
        
        Args:
            transform: 变换信息
            scene: 可选的场景，如果提供则将节点添加到场景
            name: 节点名称
            
        Returns:
            创建的变换节点
        """
        node = TransformNode(transform, name)
        if scene:
            scene.add(node)
        return node
