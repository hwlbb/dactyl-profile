"""
变换操作测试 - 展示lib.py中变换函数的使用
"""
from src.lib import *
import os

def test_translate():
    """测试平移操作"""
    shape = cube(10, 10, 10)
    moved_shape = translate(20, 5, 10)(shape)  # 将立方体平移到新位置
    render_to_file(moved_shape, 'tests/output/translated_cube.scad')
    print("已生成平移测试文件")

def test_rotate():
    """测试旋转操作"""
    shape = cube(20, 10, 5)
    # 沿X轴旋转45度
    rotated_shape = rotate_x(45)(shape)
    render_to_file(rotated_shape, 'tests/output/rotated_x_cube.scad')
    
    # 沿Y轴旋转30度
    rotated_shape = rotate_y(30)(shape)
    render_to_file(rotated_shape, 'tests/output/rotated_y_cube.scad')
    
    # 沿Z轴旋转60度
    rotated_shape = rotate_z(60)(shape)
    render_to_file(rotated_shape, 'tests/output/rotated_z_cube.scad')
    print("已生成旋转测试文件")

def test_scale():
    """测试缩放操作"""
    shape = cube(10, 10, 10)
    # 不均匀缩放
    scaled_shape = scale(2, 1, 0.5)(shape)
    render_to_file(scaled_shape, 'tests/output/scaled_cube.scad')
    print("已生成缩放测试文件")

def test_compose_transforms():
    """测试组合变换"""
    shape = cube(10, 10, 10)
    # 组合多个变换：旋转、平移、缩放
    transformed = compose(
        rotate_z(45),
        translate(0, 0, 20),
        scale(1.5, 1.5, 2)
    )(shape)
    
    render_to_file(transformed, 'tests/output/composed_transforms.scad')
    print("已生成组合变换测试文件")

def run_all_tests():
    """运行所有变换测试"""
    print("\n=== 运行变换操作测试 ===")
    test_translate()
    test_rotate()
    test_scale()
    test_compose_transforms()
    print("变换操作测试完成")

if __name__ == "__main__":
    run_all_tests()