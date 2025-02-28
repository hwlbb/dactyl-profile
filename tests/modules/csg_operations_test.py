"""
CSG操作测试 - 展示lib.py中构造实体几何操作的使用
"""
import os
import sys

# 添加项目根目录到路径
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.lib import *

# 测试输出目录
TEST_OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '../output')

def test_union():
    """测试并集操作"""
    cube1 = translate(-5, -5, 0)(cube(10, 10, 10))
    sphere1 = translate(5, 5, 5)(sphere(8))
    # 创建两个形状的并集
    united = union(cube1, sphere1)
    render_to_file(united, os.path.join(TEST_OUTPUT_DIR, 'union_example.scad'))
    print("已生成并集测试文件")

def test_difference():
    """测试差集操作"""
    main_shape = cube(20, 20, 20)
    hole = translate(10, 10, -1)(cylinder(r=5, h=22))
    # 从主体中减去孔洞
    result = difference(main_shape, hole)
    render_to_file(result, os.path.join(TEST_OUTPUT_DIR, 'difference_example.scad'))
    print("已生成差集测试文件")

def test_intersection():
    """测试交集操作"""
    cube1 = cube(20, 20, 20, center=True)
    sphere1 = sphere(15)
    # 创建两个形状的交集
    result = intersection(cube1, sphere1)
    render_to_file(result, os.path.join(TEST_OUTPUT_DIR, 'intersection_example.scad'))
    print("已生成交集测试文件")

def test_hull():
    """测试凸包操作"""
    sphere1 = translate(-10, 0, 0)(sphere(5))
    sphere2 = translate(10, 0, 0)(sphere(5))
    cylinder1 = translate(0, 10, 0)(cylinder(r=5, h=10))
    # 创建三个形状的凸包
    result = hull(sphere1, sphere2, cylinder1)
    render_to_file(result, os.path.join(TEST_OUTPUT_DIR, 'hull_example.scad'))
    print("已生成凸包测试文件")

def run_all_tests():
    """运行所有CSG操作测试"""
    print("\n=== 运行CSG操作测试 ===")
    test_union()
    test_difference()
    test_intersection()
    test_hull()
    print("CSG操作测试完成")

if __name__ == "__main__":
    # 确保测试输出目录存在
    os.makedirs(TEST_OUTPUT_DIR, exist_ok=True)
    run_all_tests()