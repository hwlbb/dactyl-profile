"""
比较测试 - 对比新旧lib实现的开关组件
"""
import os
import sys
import filecmp

# 添加项目根目录到路径
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.switches import single_switch as old_switch, sa_cap as old_cap
from src.switches_new import single_switch as new_switch, sa_cap as new_cap
from src.lib import render_to_file as old_render
from src.lib_redesign import render_to_file as new_render

# 测试输出目录
TEST_OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '../output')

def test_compare_switches():
    """比较新旧库实现的开关"""
    print("\n=== 比较开关实现 ===")
    
    # 生成旧库版本的开关
    old_switch_file = os.path.join(TEST_OUTPUT_DIR, 'old_switch.scad')
    old_render(old_switch, old_switch_file)
    
    # 生成新库版本的开关
    new_switch_file = os.path.join(TEST_OUTPUT_DIR, 'new_switch.scad')
    new_render(new_switch, new_switch_file)
    
    # 比较文件大小
    old_size = os.path.getsize(old_switch_file)
    new_size = os.path.getsize(new_switch_file)
    print(f"旧库开关文件大小: {old_size} 字节")
    print(f"新库开关文件大小: {new_size} 字节")
    
    # 文件是否完全相同
    files_identical = filecmp.cmp(old_switch_file, new_switch_file, shallow=False)
    print(f"开关文件完全相同: {'是' if files_identical else '否'}")
    
    print("已生成新旧库开关对比文件")

def test_compare_keycaps():
    """比较新旧库实现的键帽"""
    print("\n=== 比较键帽实现 ===")
    
    # 生成旧库版本的键帽
    old_cap_file = os.path.join(TEST_OUTPUT_DIR, 'old_cap.scad')
    old_render(old_cap, old_cap_file)
    
    # 生成新库版本的键帽
    new_cap_file = os.path.join(TEST_OUTPUT_DIR, 'new_cap.scad')
    new_render(new_cap, new_cap_file)
    
    # 比较文件大小
    old_size = os.path.getsize(old_cap_file)
    new_size = os.path.getsize(new_cap_file)
    print(f"旧库键帽文件大小: {old_size} 字节")
    print(f"新库键帽文件大小: {new_size} 字节")
    
    # 文件是否完全相同
    files_identical = filecmp.cmp(old_cap_file, new_cap_file, shallow=False)
    print(f"键帽文件完全相同: {'是' if files_identical else '否'}")
    
    print("已生成新旧库键帽对比文件")

def run_all_tests():
    """运行所有比较测试"""
    # 确保测试输出目录存在
    os.makedirs(TEST_OUTPUT_DIR, exist_ok=True)
    
    test_compare_switches()
    test_compare_keycaps()
    
    print("比较测试完成")

if __name__ == "__main__":
    run_all_tests()
