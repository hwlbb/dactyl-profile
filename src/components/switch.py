"""
开关组件 - 实现机械键盘开关和键帽
"""
from typing import Optional, Dict, Any, List, Tuple, Union
from ..core.scene import Scene, Node, GeometryNode, OperationNode, TransformNode
from ..core.transform import TransformSystem
from ..core.config import KeyboardConfig
from ..geometry.primitives import create_cube, create_cylinder, create_square
from ..geometry.operations import (
    create_union, create_difference, create_hull, 
    create_translate, create_rotate, create_extrude_linear
)
from .base import Component
from ..geometry import create_node_from_shape  # 添加这个导入

class SwitchComponent(Component):
    """
    键盘开关组件
    
    表示单个机械键盘开关，包括开关底座和开孔。
    """
    
    def __init__(self, config: KeyboardConfig = None):
        """
        初始化开关组件
        
        Args:
            config: 键盘配置对象，如果不提供则使用默认配置
        """
        super().__init__(config)
        
        # 缓存计算出的形状
        self._switch_shape = None
        self._filled_switch_shape = None
    
    def _create_switch_shape(self) -> Dict[str, Any]:
        """
        创建单个开关的形状
        
        Returns:
            开关形状的描述字典
        """
        if self._switch_shape is not None:
            return self._switch_shape
        
        # 从配置获取参数
        keyhole_size = self.config.switch_hole_size
        switch_rim_thickness = self.config.switch_rim_thickness
        switch_thickness = self.config.switch_thickness
        
        # 计算外部宽度
        outer_width = keyhole_size + switch_rim_thickness * 2
        
        # 创建四个边缘墙
        bottom_wall = create_cube([outer_width, switch_rim_thickness, switch_thickness])
        top_wall = create_translate(bottom_wall, 0, keyhole_size + switch_rim_thickness, 0)
        left_wall = create_cube([switch_rim_thickness, outer_width, switch_thickness])
        right_wall = create_translate(left_wall, keyhole_size + switch_rim_thickness, 0, 0)
        
        # 创建卡扣突起部分
        nub_len = 2.75
        
        # 创建圆柱体并旋转
        nub_cyl = create_translate(
            create_rotate(
                create_cylinder(radius=1, height=nub_len, center=True),
                90, [1, 0, 0]
            ),
            0, 0, -1
        )
        
        # 创建左侧卡扣立方体
        nub_cube = create_translate(
            create_cube([switch_rim_thickness, nub_len, 4], center=True),
            -switch_rim_thickness / 2, 0, 0.
        )
        
        # 创建左侧卡扣(凸包操作)
        left_nub = create_translate(
            create_hull([nub_cyl, nub_cube]),
            switch_rim_thickness, outer_width / 2, 0
        )
        
        # 创建右侧卡扣立方体
        right_nub_cube = create_translate(
            create_cube([switch_rim_thickness, nub_len, 4], center=True),
            switch_rim_thickness / 2, 0, 0
        )
        
        # 创建右侧卡扣(凸包操作)
        right_nub = create_translate(
            create_hull([nub_cyl, right_nub_cube]),
            -switch_rim_thickness + outer_width, outer_width / 2, 0
        )
        
        # 合并所有部分并居中
        switch_shape = create_translate(
            create_union([bottom_wall, top_wall, left_wall, right_wall, left_nub, right_nub]),
            -outer_width / 2, -outer_width / 2, 0
        )
        
        # 缓存计算结果
        self._switch_shape = switch_shape
        return switch_shape
    
    def _create_filled_switch_shape(self) -> Dict[str, Any]:
        """
        创建填充开关的形状（没有中间开孔）
        
        Returns:
            填充开关形状的描述字典
        """
        if self._filled_switch_shape is not None:
            return self._filled_switch_shape
        
        # 从配置获取参数
        plate_outer_width = self.config.plate_outer_width
        switch_thickness = self.config.switch_thickness
        
        # 创建简单立方体
        filled_shape = create_translate(
            create_cube([plate_outer_width, plate_outer_width, switch_thickness], center=True),
            0, 0, switch_thickness / 2.0
        )
        
        # 缓存计算结果
        self._filled_switch_shape = filled_shape
        return filled_shape
    
    def create_node(self, scene: Optional[Scene] = None, name: Optional[str] = None) -> Node:
        """
        创建表示此开关的场景节点
        
        Args:
            scene: 可选的场景，如果提供则将节点添加到场景中
            name: 节点名称
            
        Returns:
            创建的节点
        """
        # 默认名称
        if name is None:
            name = "switch"
        
        # 创建开关形状
        switch_shape = self._create_switch_shape()
        
        # 使用通用的节点创建函数来处理操作描述
        return create_node_from_shape(switch_shape, scene, name)


class FilledSwitchComponent(SwitchComponent):
    """
    填充开关组件
    
    表示没有中间开孔的填充开关，用于底板构建等场景。
    """
    
    def create_node(self, scene: Optional[Scene] = None, name: Optional[str] = None) -> Node:
        """
        创建表示此填充开关的场景节点
        
        Args:
            scene: 可选的场景，如果提供则将节点添加到场景中
            name: 节点名称
            
        Returns:
            创建的节点
        """
        # 默认名称
        if name is None:
            name = "filled_switch"
        
        # 创建填充开关形状
        filled_shape = self._create_filled_switch_shape()
        
        # 使用通用的节点创建函数
        return create_node_from_shape(filled_shape, scene, name)
