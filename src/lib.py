"""
lib.py - OpenSCAD 3D操作库
这是一个函数式编程接口，封装了Python Solid库，
使创建和操作3D对象变得更加简单直观。
"""
import solid
import os

# 默认细分段数，影响圆形物体的平滑度
default_segments = 18

# ======== 核心类 ========

class NativeSCAD():
    """
    基础包装类，包装Solid库的函数调用，支持链式操作。
    例如：translate(1,2,3)(cube(10,10,10))
    """
    def __init__(self, solid_fn, *args, **kwargs):
        # 存储函数及其参数，延迟到compile时执行
        def build_solid_fn():
            return solid_fn(*args, **kwargs)
        self.solid = build_solid_fn

    def __call__(self, other):
        """
        支持函数调用语法，例如：translate(x,y,z)(cube(...))
        """
        assert isinstance(other, NativeSCAD)
        return Composer([self, other])

    def _apply_to(self, other):
        """
        将当前变换应用到另一个对象上
        """
        return self.compile()(other)

    def compile(self):
        """
        编译为实际的OpenSCAD对象
        """
        return self.solid()


class Composer(NativeSCAD):
    """
    组合多个操作的类，按顺序应用变换
    例如：translate(...)(rotate(...)(cube(...)))
    """
    def __init__(self, children):
        assert len(children) > 0
        self.children = children

    def _apply_to(self, other):
        """
        从后向前应用所有变换
        """
        result = other
        for c in reversed(self.children):
            result = c._apply_to(result)
        return result

    def compile(self):
        """
        编译整个变换链
        """
        # 从最后一个操作开始，逐步向前应用每个变换
        # result = self.children[-1].compile()
        
        # for c in reversed(self.children[:-1]):
        #     result = c._apply_to(result)
        # return result

        result = self.children[1].compile()
        result = self.children[0]._apply_to(result)
        return result


class Merger(NativeSCAD):
    """
    处理合并操作的类，如union()、difference()等
    """
    def __init__(self, solid_fn, children):
        self.solid = solid_fn
        self.children = children

    def __call__(self, other):
        raise RuntimeError('无法对合并操作执行调用')

    def _apply_to(self, other):
        raise RuntimeError('无法对其他对象应用合并操作')

    def compile(self):
        """
        编译所有子对象并合并
        """
        return self.solid()(*[c.compile() for c in self.children])


# ======== 变换函数 ========

def translate(x, y, z):
    """平移变换，移动对象到新位置"""
    return NativeSCAD(solid.translate, [x, y, z])

def identity():
    """恒等变换，不做任何改变"""
    return translate(0, 0, 0)

def scale(x, y, z):
    """缩放变换"""
    return NativeSCAD(solid.scale, [x, y, z])

def rotate(*, a, v):
    """绕任意轴旋转"""
    return NativeSCAD(solid.rotate, a=a, v=v)

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
    """镜像变换，根据给定向量创建对象的镜像"""
    return NativeSCAD(solid.mirror, [x, y, z])

def flip_lr():
    """水平翻转（左右镜像）"""
    return mirror(-1, 0, 0)


# ======== 工具函数 ========

def project(*args, **kwargs):
    """将3D对象投影到2D平面"""
    return NativeSCAD(solid.projection, *args, **kwargs)

def offset(*args):
    """2D偏移操作，可用于放大或缩小2D形状"""
    return NativeSCAD(solid.offset, *args)

def extrude_linear(height):
    """线性拉伸2D形状为3D对象"""
    return NativeSCAD(solid.linear_extrude, height)

def colour(r, g, b, z):
    """设置颜色，r,g,b为0-255值，z为透明度(0-1)"""
    return NativeSCAD(solid.color, [r/255.0, g/255.0, b/255.0, z])


# ======== 函数式组合 ========

def compose(*atoms):
    """
    组合多个变换为一个单一变换
    例如：compose(translate(...), rotate_x(...), scale(...))
    """
    assert len(atoms) > 0
    return Composer(list(reversed(atoms)))


# ======== CSG操作 ========

def union(*children):
    """合并多个对象为一个整体"""
    return Merger(solid.union, children)

def hull(*children):
    """创建包含所有给定对象的凸包"""
    return Merger(solid.hull, children)

def difference(*children):
    """从第一个对象中减去其他所有对象"""
    return Merger(solid.difference, children)

def intersection(*children):
    """创建所有对象的交集部分"""
    return Merger(solid.intersection, children)


# ======== 基础形状 ========

def cube(x, y, z, **kwargs):
    """创建长方体"""
    return NativeSCAD(solid.cube, [x, y ,z], **kwargs)

def cylinder(r, h, segments=default_segments, **kwargs):
    """创建圆柱体，r为半径，h为高度"""
    return NativeSCAD(solid.cylinder, r=r, h=h, segments=segments, **kwargs)

def cylinderr1r2(r1, r2, h, segments=default_segments, **kwargs):
    """创建圆台，r1为底部半径，r2为顶部半径，h为高度"""
    return NativeSCAD(solid.cylinder, r1=r1, r2=r2, h=h, segments=segments, **kwargs)

def sphere(r, segments=default_segments, **kwargs):
    """创建球体，r为半径"""
    return NativeSCAD(solid.sphere, r=r, segments=segments, **kwargs)

def square(x, y, **kwargs):
    """创建2D矩形"""
    return NativeSCAD(solid.square, [x, y], **kwargs)


# ======== 输出函数 ========

def render_to_file(obj, filename):
    """
    将3D模型渲染为OpenSCAD文件
    obj: NativeSCAD对象
    filename: 输出文件路径
    """
    # 确保filename是字符串
    if filename is None:
        raise ValueError("输出文件名不能为None")
    
    # 获取文件路径和文件名
    filepath = str(filename)
    out_dir = os.path.dirname(os.path.abspath(filepath))
    
    # 确保目录存在
    os.makedirs(out_dir, exist_ok=True)
    
    # 将obj编译为OpenSCAD对象，并输出到文件
    # 显式提供out_dir参数
    solid.scad_render_to_file(obj.compile(), filepath=filepath, out_dir=out_dir)
