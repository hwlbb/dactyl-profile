import numpy as np
from math import radians, sin, cos

def point3(x, y, z):
    """创建一个3D点（使用标准的列向量形式）"""
    return np.transpose(np.array([[x, y, z, 1]]))

def vec3(x, y, z):
    """创建一个3D向量（使用标准的列向量形式）"""
    return np.transpose(np.array([[x, y, z, 0]]))

def to_point(pv):
    """从齐次坐标转换回3D坐标"""
    return pv.flatten()[:3]

def translate(x, y, z):
    """创建平移矩阵"""
    return np.array([
        [1, 0, 0, x],
        [0, 1, 0, y],
        [0, 0, 1, z],
        [0, 0, 0, 1],
    ])

def scale(x, y, z):
    """创建缩放矩阵"""
    return np.array([
        [x, 0, 0, 0],
        [0, y, 0, 0],
        [0, 0, z, 0],
        [0, 0, 0, 1],
    ])

def identity():
    """创建单位矩阵"""
    return scale(1, 1, 1)

def rotate_x(deg):
    """创建绕X轴旋转的矩阵"""
    rad = radians(deg)
    return np.array([
        [1, 0, 0, 0],
        [0, cos(rad), -sin(rad), 0],
        [0, sin(rad), cos(rad), 0],
        [0, 0, 0, 1],
    ])

def rotate_y(deg):
    """创建绕Y轴旋转的矩阵"""
    rad = radians(deg)
    return np.array([
        [cos(rad), 0, sin(rad), 0],
        [0, 1, 0, 0],
        [-sin(rad), 0, cos(rad), 0],
        [0, 0, 0, 1],
    ])

def rotate_z(deg):
    """创建绕Z轴旋转的矩阵"""
    rad = radians(deg)
    return np.array([
        [cos(rad), -sin(rad), 0, 0],
        [sin(rad), cos(rad), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1],
    ])

def compose(*mats):
    """组合多个变换矩阵"""
    result = identity()
    for m in mats:
        result = m @ result
    return result
