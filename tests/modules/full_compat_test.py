"""
全面兼容性测试 - 验证新库能否正常生成键盘
"""
import os
import sys
import time

# 添加项目根目录到路径
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.case_utils import right_shell, bottom_plate
from src.lib import render_to_file

# 测试输出目录
TEST_OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '../output')

def test_full_keyboard_gen():
    """测试生成完整键盘模型"""
    print("\n=== 测试完整键盘生成 ===")
    start_time = time.time()
    
    # 生成右侧键盘壳体
    print("生成右侧壳体...")
    shell_file = os.path.join(TEST_OUTPUT_DIR, 'test_right_shell.scad')
    render_to_file(right_shell(), shell_file)
    
    # 生成底板
    print("生成底板...")
    plate_file = os.path.join(TEST_OUTPUT_DIR, 'test_bottom_plate.scad')
    render_to_file(bottom_plate(), plate_file)
    
    end_time = time.time()
    print(f"键盘文件生成完成，耗时: {end_time - start_time:.2f}秒")
    print(f"文件保存在: {TEST_OUTPUT_DIR}")

def run_all_tests():
    """运行所有全面测试"""
    # 确保测试输出目录存在
    os.makedirs(TEST_OUTPUT_DIR, exist_ok=True)
    
    test_full_keyboard_gen()
    print("全面兼容性测试完成")

if __name__ == "__main__":
    run_all_tests()
