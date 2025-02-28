"""
多元素Composer测试 - 明确展示compose函数创建的多元素Composer
"""
import os
import sys

# 添加项目根目录到路径
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.lib import *

# 测试输出目录
TEST_OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '../output')

def test_compose_multi_elements():
    """测试compose函数创建的多元素Composer"""
    print("\n=== 测试compose多元素结构 ===")
    
    # 创建一个具有多个变换的compose
    multi_transform = compose(
        translate(10, 0, 0),
        rotate_z(45),
        rotate_y(30),
        scale(2, 2, 1)
    )
    
    # 直接检查并打印Composer对象的children
    print(f"Composer类型: {type(multi_transform)}")
    print(f"Composer.children长度: {len(multi_transform.children)}")
    print("Composer.children列表内容:")
    for i, child in enumerate(multi_transform.children):
        print(f"  元素{i}: {type(child)} - {child}")
    
    # 应用变换并渲染
    result = multi_transform(cube(10, 10, 10))
    render_to_file(result, os.path.join(TEST_OUTPUT_DIR, 'multi_compose.scad'))
    
    print("测试完成")

def run_all_tests():
    """运行所有多元素Composer测试"""
    # 确保测试输出目录存在
    os.makedirs(TEST_OUTPUT_DIR, exist_ok=True)
    
    test_compose_multi_elements()

if __name__ == "__main__":
    run_all_tests()
