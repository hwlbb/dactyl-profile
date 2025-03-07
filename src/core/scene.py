"""
场景图系统 - 提供基于节点的3D场景管理

这是整个系统的核心架构，采用场景图模式组织3D对象，
类似于现代3D引擎和CAD系统的设计方式。
"""
import uuid
import solid
from typing import List, Dict, Any, Optional, Union, Callable


class Node:
    """
    场景图中的基本节点
    
    所有场景对象都从此类派生。节点可以有父节点和子节点，
    形成一个层次结构，便于管理场景中的对象关系。
    """
    
    def __init__(self, name: str = None):
        """
        初始化节点
        
        Args:
            name: 节点名称，如果不提供则自动生成
        """
        self.id = str(uuid.uuid4())
        self.name = name or f"node_{self.id[:8]}"
        self.children: List[Node] = []
        self.parent: Optional[Node] = None
        self.visible = True
        self.metadata: Dict[str, Any] = {}
    
    def add(self, child: 'Node') -> 'Node':
        """
        添加子节点
        
        Args:
            child: 要添加的子节点
            
        Returns:
            添加的子节点，便于链式调用
        """
        # 如果节点已经有父节点，先从原父节点移除
        if child.parent:
            child.parent.remove(child)
            
        self.children.append(child)
        child.parent = self
        return child
    
    def remove(self, child: 'Node') -> bool:
        """
        移除子节点
        
        Args:
            child: 要移除的子节点
            
        Returns:
            是否成功移除
        """
        if child in self.children:
            self.children.remove(child)
            child.parent = None
            return True
        return False
    
    def find_by_name(self, name: str) -> Optional['Node']:
        """
        通过名称查找节点
        
        Args:
            name: 要查找的节点名称
            
        Returns:
            找到的节点或None
        """
        if self.name == name:
            return self
            
        for child in self.children:
            result = child.find_by_name(name)
            if result:
                return result
                
        return None
    
    def compile(self):
        """
        编译节点为最终的几何体
        
        Returns:
            编译后的OpenSCAD对象
        """
        raise NotImplementedError("子类必须实现compile方法")


class TransformNode(Node):
    """
    变换节点 - 对子节点应用变换
    
    例如平移、旋转、缩放等。变换节点不包含几何体，
    仅对其子节点应用变换。
    """
    
    def __init__(self, transform_data: Dict[str, Any], name: str = None):
        """
        初始化变换节点
        
        Args:
            transform_data: 变换数据，包含类型和参数
            name: 节点名称
        """
        super().__init__(name or f"transform_{transform_data['type']}")
        self.transform_data = transform_data
    
    def compile(self):
        """
        编译变换节点及其子节点
        
        Returns:
            应用了变换的OpenSCAD对象
        """
        # 首先编译所有子节点并合并
        children_compiled = [child.compile() for child in self.children if child.visible]
        if not children_compiled:
            return None
            
        result = solid.union()(*children_compiled)
        
        # 根据变换类型应用不同的变换
        transform_type = self.transform_data['type']
        
        if transform_type == 'translate':
            return solid.translate(self.transform_data['args'])(result)
        elif transform_type == 'rotate_x':
            return solid.rotate(a=self.transform_data['args'][0], v=[1, 0, 0])(result)
        elif transform_type == 'rotate_y':
            return solid.rotate(a=self.transform_data['args'][0], v=[0, 1, 0])(result)
        elif transform_type == 'rotate_z':
            return solid.rotate(a=self.transform_data['args'][0], v=[0, 0, 1])(result)
        elif transform_type == 'rotate':
            return solid.rotate(a=self.transform_data['angle'], v=self.transform_data['axis'])(result)
        elif transform_type == 'scale':
            return solid.scale(self.transform_data['args'])(result)
        elif transform_type == 'projection':
            return solid.projection(cut=self.transform_data.get('cut', False))(result)
        elif transform_type == 'extrude_linear':
            return solid.linear_extrude(height=self.transform_data['height'])(result)
        else:
            # 未知变换类型，返回原始结果
            return result


class GeometryNode(Node):
    """
    几何体节点 - 包含实际的几何形状
    """
    
    def __init__(self, shape_data: Dict[str, Any], name: str = None):
        """
        初始化几何体节点
        
        Args:
            shape_data: 形状数据，包含类型和参数
            name: 节点名称
        """
        super().__init__(name or f"geometry_{shape_data['type']}")
        self.shape_data = shape_data
    
    def compile(self):
        """
        编译几何体节点
        
        Returns:
            OpenSCAD几何体对象
        """
        # 根据形状类型创建不同的几何体
        shape_type = self.shape_data['type']
        params = self.shape_data['params']
        
        if shape_type == 'cube':
            return solid.cube(params['size'], center=params.get('center', False))
        elif shape_type == 'sphere':
            return solid.sphere(r=params['radius'], segments=params.get('segments', 30))
        elif shape_type == 'cylinder':
            return solid.cylinder(
                h=params['height'], 
                r=params.get('radius'), 
                r1=params.get('radius1'),
                r2=params.get('radius2'),
                segments=params.get('segments', 30),
                center=params.get('center', False)
            )
        elif shape_type == 'square':
            # 添加对square类型的支持
            return solid.square(params['size'], center=params.get('center', False))
        # 将来添加更多形状类型
        else:
            raise ValueError(f"未知的几何体类型: {shape_type}")


class OperationNode(Node):
    """
    操作节点 - 对子节点执行布尔操作
    """
    
    def __init__(self, operation: str, name: str = None):
        """
        初始化操作节点
        
        Args:
            operation: 操作类型，如'union', 'difference', 'hull'等
            name: 节点名称
        """
        super().__init__(name or f"{operation}_op")
        self.operation = operation
    
    def compile(self):
        """
        编译操作节点及其子节点
        
        Returns:
            布尔操作后的OpenSCAD对象
        """
        # 编译所有可见的子节点
        children_compiled = [child.compile() for child in self.children if child.visible]
        
        if not children_compiled:
            return None
        
        # 根据操作类型执行不同的布尔操作
        if self.operation == 'union':
            return solid.union()(*children_compiled)
        elif self.operation == 'difference':
            return solid.difference()(*children_compiled)
        elif self.operation == 'intersection':
            return solid.intersection()(*children_compiled)
        elif self.operation == 'hull':
            return solid.hull()(*children_compiled)
        else:
            raise ValueError(f"未知的操作类型: {self.operation}")


class Scene:
    """
    场景 - 管理整个场景图
    
    场景是所有节点的根容器，提供全局操作和管理功能。
    """
    
    def __init__(self, name: str = "main_scene"):
        """
        初始化场景
        
        Args:
            name: 场景名称
        """
        self.name = name
        self.root = Node(name="root")
    
    def add(self, node: Node) -> Node:
        """
        向场景添加节点
        
        Args:
            node: 要添加的节点
            
        Returns:
            添加的节点，便于链式调用
        """
        return self.root.add(node)
    
    def find_by_name(self, name: str) -> Optional[Node]:
        """
        通过名称查找节点
        
        Args:
            name: 要查找的节点名称
            
        Returns:
            找到的节点或None
        """
        return self.root.find_by_name(name)
    
    def compile(self):
        """
        编译整个场景
        
        Returns:
            编译后的OpenSCAD对象
        """
        # 合并所有子节点
        children_compiled = [child.compile() for child in self.root.children if child.visible]
        
        if not children_compiled:
            return None
            
        return solid.union()(*children_compiled)
    
    def render_to_file(self, filepath: str):
        """
        将场景渲染到文件
        
        Args:
            filepath: 输出文件路径
        """
        import os
        
        # 确保输出目录存在
        os.makedirs(os.path.dirname(os.path.abspath(filepath)), exist_ok=True)
        
        # 编译并渲染
        compiled = self.compile()
        if compiled:
            solid.scad_render_to_file(compiled, filepath)
