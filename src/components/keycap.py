"""
键帽组件 - 实现各种类型的键帽
"""
from typing import Optional, Dict, Any, List, Tuple, Union
from ..core.scene import Scene, Node, GeometryNode, OperationNode
from ..core.config import KeyboardConfig
from ..geometry.primitives import create_square
from ..geometry.operations import (
    create_hull, create_translate, create_extrude_linear
)
from .base import Component
from ..geometry import create_node_from_shape

class KeycapComponent(Component):
    """
    键帽组件的基类
    
    定义键帽的基本接口和共同属性。
    """
    
    def __init__(self, config: KeyboardConfig = None):
        """
        初始化键帽组件
        
        Args:
            config: 键盘配置对象，如果不提供则使用默认配置
        """
        super().__init__(config)
        self._keycap_shape = None
    
    def _create_keycap_shape(self) -> Dict[str, Any]:
        """
        创建键帽的形状
        
        Returns:
            键帽形状的描述字典
            
        Raises:
            NotImplementedError: 子类需要实现此方法
        """
        raise NotImplementedError("子类必须实现_create_keycap_shape方法")
    
    def create_node(self, scene: Optional[Scene] = None, name: Optional[str] = None) -> Node:
        """
        创建表示此键帽的场景节点
        
        Args:
            scene: 可选的场景，如果提供则将节点添加到场景中
            name: 节点名称
            
        Returns:
            创建的节点
        """
        # 默认名称
        if name is None:
            name = "keycap"
        
        # 创建键帽形状
        keycap_shape = self._create_keycap_shape()
        
        # 使用辅助函数创建节点
        return create_node_from_shape(keycap_shape, scene, name)


class SAKeycapComponent(KeycapComponent):
    """
    SA键帽组件
    
    表示SA轮廓的键帽，通常用于人体工程学键盘。
    """
    
    def _create_keycap_shape(self) -> Dict[str, Any]:
        """
        创建SA键帽的形状
        
        Returns:
            SA键帽形状的描述字典
        """
        if self._keycap_shape is not None:
            return self._keycap_shape
        
        # 从配置获取参数
        sa_length = self.config.sa_top_length
        switch_thickness = self.config.switch_thickness
        
        # 创建键帽的底部、中部和顶部
        m = 17.0  # 中部宽度
        
        # 底部是一个扁平的正方形
        bot = create_extrude_linear(
            create_square([sa_length, sa_length], center=True),
            0.1
        )
        
        # 中部是一个扁平的正方形，较小，位于中间高度
        mid = create_translate(
            create_extrude_linear(
                create_square([m, m], center=True),
                0.1
            ),
            0, 0, 6
        )
        
        # 顶部是一个扁平的正方形，最小，位于顶部
        top = create_translate(
            create_extrude_linear(
                create_square([12, 12], center=True),
                0.1
            ),
            0, 0, 12
        )
        
        # 使用凸包操作合并三个形状，创建键帽轮廓
        # 然后上移到开关顶部
        keycap_shape = create_translate(
            create_hull([bot, mid, top]),
            0, 0, 5 + switch_thickness
        )
        
        # 缓存计算结果
        self._keycap_shape = keycap_shape
        return keycap_shape
