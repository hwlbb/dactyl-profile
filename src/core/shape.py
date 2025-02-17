import solid

class Shape:
    """基础形状类，代表一个3D对象"""
    def __init__(self, shape_type: str, params: dict):
        self.type = shape_type
        self.params = params
        self.transforms = []

    def translate(self, x, y, z):
        """移动形状"""
        self.transforms.append(('translate', [x, y, z]))
        return self

    def rotate_x(self, angle):
        """绕X轴旋转"""
        self.transforms.append(('rotate_x', angle))
        return self

    def rotate_y(self, angle):
        """绕Y轴旋转"""
        self.transforms.append(('rotate_y', angle))
        return self

    def rotate_z(self, angle):
        """绕Z轴旋转"""
        self.transforms.append(('rotate_z', angle))
        return self

    def scale(self, x, y, z):
        """缩放形状"""
        self.transforms.append(('scale', [x, y, z]))
        return self

    def build(self):
        """构建OpenSCAD对象"""
        # 1. 创建基础形状
        result = self._create_base_shape()
        
        # 2. 应用变换
        for transform_type, params in self.transforms:
            result = self._apply_transform(result, transform_type, params)
        
        return result

    def _create_base_shape(self):
        """创建基础形状"""
        if self.type == 'cube':
            return solid.cube(self.params['size'])
        elif self.type == 'sphere':
            return solid.sphere(r=self.params['radius'])
        elif self.type == 'cylinder':
            return solid.cylinder(r=self.params['radius'], h=self.params['height'])
        else:
            raise ValueError(f"未知的形状类型: {self.type}")

    def _apply_transform(self, shape, transform_type, params):
        """应用变换"""
        if transform_type == 'translate':
            return solid.translate(params)(shape)
        elif transform_type == 'rotate_x':
            return solid.rotate(a=params, v=(1.0, 0.0, 0.0))(shape)
        elif transform_type == 'rotate_y':
            return solid.rotate(a=params, v=(0.0, 1.0, 0.0))(shape)
        elif transform_type == 'rotate_z':
            return solid.rotate(a=params, v=(0.0, 0.0, 1.0))(shape)
        elif transform_type == 'scale':
            return solid.scale(params)(shape)
        else:
            raise ValueError(f"未知的变换类型: {transform_type}") 