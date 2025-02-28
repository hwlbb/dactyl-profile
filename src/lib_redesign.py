"""
lib_redesign.py - 重新设计的OpenSCAD 3D操作库
这是一个更简洁直观的函数式接口，封装了Python Solid库
"""
import solid
import os

# 默认细分段数，影响圆形物体的平滑度
default_segments = 18

# ======== 核心类 ========

class OpenSCADObject:
    """
    所有OpenSCAD对象的基础接口
    定义了编译和应用的公共方法
    """
    def compile(self):
        """编译为OpenSCAD对象"""
        raise NotImplementedError("子类必须实现compile方法")
        
    def __call__(self, other):
        """支持函数调用语法，应用变换到其他对象"""
        raise NotImplementedError("子类必须实现__call__方法")


class Shape(OpenSCADObject):
    """
    基础形状类（立方体、球体等）
    """
    def __init__(self, solid_fn, *args, **kwargs):
        # 存储形状函数和参数
        self.solid_fn = solid_fn
        self.args = args
        self.kwargs = kwargs
    
    def compile(self):
        """编译为OpenSCAD对象"""
        return self.solid_fn(*self.args, **self.kwargs)
    
    def __call__(self, other):
        """形状不能直接应用于其他对象"""
        raise TypeError("形状对象不能直接应用于其他对象")


class Transform(OpenSCADObject):
    """
    变换类（平移、旋转等）
    """
    def __init__(self, solid_fn, *args, **kwargs):
        # 存储变换函数和参数
        self.solid_fn = solid_fn
        self.args = args
        self.kwargs = kwargs
    
    def compile(self):
        """编译为OpenSCAD函数对象"""
        return self.solid_fn(*self.args, **self.kwargs)
    
    def __call__(self, other):
        """应用变换到其他对象"""
        if not isinstance(other, OpenSCADObject):
            raise TypeError("变换只能应用于OpenSCAD对象")
            
        # 创建变换链
        return TransformChain([self, other])
    
    def apply_to(self, scad_obj):
        """应用变换到已编译的OpenSCAD对象"""
        return self.compile()(scad_obj)


class TransformChain(OpenSCADObject):
    """
    变换链类，支持链式变换或多变换组合
    """
    def __init__(self, objects):
        self.objects = objects
    
    def compile(self):
        """编译整个变换链"""
        # 简单情况：只有两个元素（一个变换一个对象）
        if len(self.objects) == 2:
            # 先编译最后一个对象（形状或另一个变换链）
            result = self.objects[1].compile()
            # 然后应用第一个变换
            return self.objects[0].apply_to(result)
        
        # 复杂情况：多个变换
        result = self.objects[-1].compile()  # 从形状开始
        # 从后向前应用每个变换
        for transform in reversed(self.objects[:-1]):
            result = transform.apply_to(result)
        return result
    
    def __call__(self, other):
        """继续链式调用，添加新对象到变换链"""
        if not isinstance(other, OpenSCADObject):
            raise TypeError("变换只能应用于OpenSCAD对象")
            
        return TransformChain([self, other])


class CSGOperation(OpenSCADObject):
    """
    CSG操作类（并集、差集等）
    """
    def __init__(self, solid_fn, children):
        self.solid_fn = solid_fn
        self.children = children
    
    def compile(self):
        """编译所有子对象并执行CSG操作"""
        return self.solid_fn()(*[c.compile() for c in self.children])
    
    def __call__(self, other):
        """CSG操作不能直接应用于对象"""
        raise TypeError("CSG操作不能直接应用于对象")


# ======== 变换函数 ========

def translate(x, y, z):
    """平移变换"""
    return Transform(solid.translate, [x, y, z])

def identity():
    """恒等变换"""
    return translate(0, 0, 0)

def scale(x, y, z):
    """缩放变换"""
    return Transform(solid.scale, [x, y, z])

def rotate(*, a, v):
    """绕任意轴旋转"""
    return Transform(solid.rotate, a=a, v=v)

def rotate_x(a):
    """绕X轴旋转a度"""
    return rotate(a=a, v=[1, 0, 0])

def rotate_y(a):
    """绕Y轴旋转a度"""
    return rotate(a=a, v=[0, 1, 0])

def rotate_z(a):
    """绕Z轴旋转a度"""
    return rotate(a=a, v=[0, 0, 1])

def mirror(x, y, z):
    """镜像变换"""
    return Transform(solid.mirror, [x, y, z])

def flip_lr():
    """水平翻转"""
    return mirror(-1, 0, 0)

# ======== 工具函数 ========

def project(*args, **kwargs):
    """2D投影"""
    return Transform(solid.projection, *args, **kwargs)

def offset(*args):
    """2D偏移操作"""
    return Transform(solid.offset, *args)

def extrude_linear(height):
    """拉伸操作"""
    return Transform(solid.linear_extrude, height)

def colour(r, g, b, z=1):
    """上色操作"""
    return Transform(solid.color, [r/255.0, g/255.0, b/255.0, z])

# ======== 函数式组合 ========

def compose(*transforms):
    """组合多个变换为一个变换链"""
    if not transforms:
        raise ValueError("compose需要至少一个变换")
    
    # 按从内向外的顺序排列（与原代码一致）
    return TransformChain(list(reversed(transforms)))

# ======== CSG操作 ========

def union(*children):
    """并集操作"""
    return CSGOperation(solid.union, children)

def hull(*children):
    """凸包操作"""
    return CSGOperation(solid.hull, children)

def difference(*children):
    """差集操作"""
    return CSGOperation(solid.difference, children)

def intersection(*children):
    """交集操作"""
    return CSGOperation(solid.intersection, children)

# ======== 基础形状 ========

def cube(x, y, z, **kwargs):
    """创建立方体"""
    return Shape(solid.cube, [x, y, z], **kwargs)

def cylinder(r, h, segments=default_segments, **kwargs):
    """创建圆柱体"""
    return Shape(solid.cylinder, r=r, h=h, segments=segments, **kwargs)

def cylinderr1r2(r1, r2, h, segments=default_segments, **kwargs):
    """创建圆台"""
    return Shape(solid.cylinder, r1=r1, r2=r2, h=h, segments=segments, **kwargs)

def sphere(r, segments=default_segments, **kwargs):
    """创建球体"""
    return Shape(solid.sphere, r=r, segments=segments, **kwargs)

def square(x, y, **kwargs):
    """创建矩形"""
    return Shape(solid.square, [x, y], **kwargs)

# ======== 输出函数 ========

def render_to_file(obj, filename):
    """将对象渲染到文件"""
    if filename is None:
        raise ValueError("输出文件名不能为None")
    
    filepath = str(filename)
    out_dir = os.path.dirname(os.path.abspath(filepath))
    os.makedirs(out_dir, exist_ok=True)
    
    solid.scad_render_to_file(obj.compile(), filepath=filepath, out_dir=out_dir)
