from typing import List
from .shape import Shape

class CombinedShape(Shape):
    """组合形状类"""
    def __init__(self, shapes: List[Shape], operation: str):
        super().__init__('combined', {
            'operation': operation,
            'shapes': shapes
        })

    def _create_base_shape(self):
        import solid
        # 构建所有子形状
        built_shapes = [shape.build() for shape in self.params['shapes']]
        
        # 应用组合操作
        if self.params['operation'] == 'union':
            return solid.union()(*built_shapes)
        elif self.params['operation'] == 'difference':
            return solid.difference()(*built_shapes)
        elif self.params['operation'] == 'intersection':
            return solid.intersection()(*built_shapes)
        else:
            raise ValueError(f"未知的组合操作: {self.params['operation']}")

def union(*shapes: Shape) -> CombinedShape:
    """合并多个形状"""
    return CombinedShape(list(shapes), 'union')

def difference(base: Shape, *shapes: Shape) -> CombinedShape:
    """从base中减去其他形状"""
    return CombinedShape([base, *shapes], 'difference')

def intersection(*shapes: Shape) -> CombinedShape:
    """获取多个形状的交集"""
    return CombinedShape(list(shapes), 'intersection') 