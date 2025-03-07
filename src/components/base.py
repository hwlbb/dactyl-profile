"""
组件基类 - 定义键盘组件的基础接口
"""
from typing import Any, Dict, List, Optional, Tuple, Union
from ..core.scene import Node, Scene
from ..core.config import KeyboardConfig

class Component:
    """
    键盘组件的基础类
    
    所有具体键盘部件都应该继承这个类，实现通用接口。
    """
    
    def __init__(self, config: KeyboardConfig = None):
        """
        初始化组件
        
        Args:
            config: 键盘配置对象，如果不提供则使用默认配置
        """
        self.config = config or KeyboardConfig.create_default()
        self.metadata: Dict[str, Any] = {}
    
    def create_node(self, scene: Optional[Scene] = None, name: Optional[str] = None) -> Node:
        """
        创建表示此组件的场景节点
        
        Args:
            scene: 可选的场景，如果提供则将节点添加到场景中
            name: 节点名称
            
        Returns:
            创建的节点
            
        Raises:
            NotImplementedError: 子类需要实现此方法
        """
        raise NotImplementedError("子类必须实现create_node方法")
    
    def set_metadata(self, key: str, value: Any) -> None:
        """
        设置组件元数据
        
        Args:
            key: 元数据键
            value: 元数据值
        """
        self.metadata[key] = value
    
    def get_metadata(self, key: str, default: Any = None) -> Any:
        """
        获取组件元数据
        
        Args:
            key: 元数据键
            default: 默认值，如果键不存在则返回此值
            
        Returns:
            元数据值或默认值
        """
        return self.metadata.get(key, default)
