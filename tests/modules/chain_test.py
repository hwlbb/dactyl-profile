"""
链式操作测试 - 展示lib.py中的链式操作如何工作
"""
import os
import sys

# 添加项目根目录到路径
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.lib import *

# 测试输出目录
TEST_OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '../output')

def test_complex_chain():
    """测试复杂的链式操作"""
    print("\n=== 测试复杂链式操作 ===")
    
    # 创建一个简单的立方体
    box = cube(10, 10, 10)
    print("创建基础立方体")
    
    # 缩放操作
    scaled = scale(2, 2, 2)(box)
    print("应用缩放后...")
    
    # 旋转操作
    rotated = rotate_z(45)(scaled)
    print("应用旋转后...")
    
    # 平移操作
    translated = translate(10, 0, 0)(rotated)
    print("应用平移后...")
    
    # 渲染最终结果
    render_to_file(translated, os.path.join(TEST_OUTPUT_DIR, 'complex_chain.scad'))
    print("已生成复杂链式操作测试文件")

def run_all_tests():
    """运行所有链式操作测试"""
    # 确保测试输出目录存在
    os.makedirs(TEST_OUTPUT_DIR, exist_ok=True)
    
    test_complex_chain()
    print("链式操作测试完成")

if __name__ == "__main__":
    run_all_tests()
