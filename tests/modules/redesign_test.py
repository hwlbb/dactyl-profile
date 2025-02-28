"""
Lib重新设计测试 - 测试新库是否能正常工作
"""
import os
import sys

# 添加项目根目录到路径
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.shapes_new import *
from src.lib_redesign import render_to_file

# 测试输出目录
TEST_OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '../output')

def test_basic_shapes():
    """测试使用新库创建的基础形状"""
    # 测试球体
    render_to_file(switch_riser_raw_dot, os.path.join(TEST_OUTPUT_DIR, 'redesign_dot.scad'))
    
    # 测试组合形状
    render_to_file(switch_riser_post, os.path.join(TEST_OUTPUT_DIR, 'redesign_post.scad'))
    
    print("已生成使用新库的基础形状")

def run_all_tests():
    """运行所有重新设计测试"""
    # 确保测试输出目录存在
    os.makedirs(TEST_OUTPUT_DIR, exist_ok=True)
    
    test_basic_shapes()
    print("重新设计库测试完成")

if __name__ == "__main__":
    run_all_tests()
