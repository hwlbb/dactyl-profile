"""
基础形状测试 - 展示lib.py中基本形状创建函数的使用
"""
import os
import sys

# 添加项目根目录到路径
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.lib import *

# 测试输出目录
TEST_OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '../output')

def test_cube():
    """测试立方体创建"""
    shape = cube(10, 20, 15)  # 创建10x20x15的长方体
    render_to_file(shape, os.path.join(TEST_OUTPUT_DIR, 'cube.scad'))
    print("已生成立方体测试文件")

def test_cylinder():
    """测试圆柱体创建"""
    shape = cylinder(r=10, h=20)  # 创建半径10,高20的圆柱
    render_to_file(shape, os.path.join(TEST_OUTPUT_DIR, 'cylinder.scad'))
    print("已生成圆柱体测试文件")

def test_sphere():
    """测试球体创建"""
    shape = sphere(r=15)  # 创建半径15的球体
    render_to_file(shape, os.path.join(TEST_OUTPUT_DIR, 'sphere.scad'))
    print("已生成球体测试文件")

def test_centered_shapes():
    """测试居中创建形状"""
    centered_cube = cube(10, 10, 10, center=True)  # 创建居中的立方体
    render_to_file(centered_cube, os.path.join(TEST_OUTPUT_DIR, 'centered_cube.scad'))
    print("已生成居中立方体测试文件")

def run_all_tests():
    """运行所有基础形状测试"""
    print("\n=== 运行基础形状测试 ===")
    test_cube()
    test_cylinder()
    test_sphere()
    test_centered_shapes()
    print("基础形状测试完成")

if __name__ == "__main__":
    # 确保测试输出目录存在
    os.makedirs(TEST_OUTPUT_DIR, exist_ok=True)
    run_all_tests()