"""
键帽测试 - 使用lib.py创建简单的键帽模型
"""
from src.lib import *
import os

def create_simple_keycap(width=18, height=18, top_width=12, profile_height=10):
    """创建一个简单的斜角键帽"""
    # 底部
    bottom = square(width, height, center=True)
    bottom = extrude_linear(0.1)(bottom)
    
    # 顶部
    top = square(top_width, top_width, center=True)
    top = extrude_linear(0.1)(top)
    top = translate(0, 0, profile_height)(top)
    
    # 使用hull操作连接底部和顶部，形成斜角形状
    keycap = hull(bottom, top)
    
    # 添加基本颜色
    return colour(200, 200, 200, 1)(keycap)

def test_simple_keycap():
    """测试简单键帽生成"""
    keycap = create_simple_keycap()
    render_to_file(keycap, 'tests/output/simple_keycap.scad')
    print("已生成简单键帽测试文件")

def test_keycap_row():
    """测试生成一排键帽"""
    # 创建一排5个键帽
    keycaps = []
    spacing = 20
    
    for i in range(5):
        pos = translate(i * spacing, 0, 0)
        # 为每个键帽分配不同颜色
        color = colour(200, 150 + i*20, 150 + i*20, 1)
        keycap = pos(color(create_simple_keycap()))
        keycaps.append(keycap)
    
    row = union(*keycaps)
    render_to_file(row, 'tests/output/keycap_row.scad')
    print("已生成键帽行测试文件")

def test_curved_keycap_row():
    """测试生成弯曲的键帽行"""
    # 创建弯曲的一排5个键帽
    keycaps = []
    spacing = 20
    radius = 70  # 曲率半径
    
    for i in range(5):
        # 计算弧形布局的角度
        angle = -10 + i * 5  # 从-10度到10度
        
        # 使用旋转和平移放置键帽
        pos = compose(
            rotate_y(angle),  
            translate(0, 0, radius),  # 移动到半径位置
            translate(0, 0, -radius)  # 恢复原来的高度
        )
        
        # 为每个键帽分配不同颜色
        color = colour(200, 150 + i*20, 150 + i*20, 1)
        keycap = pos(color(create_simple_keycap()))
        keycaps.append(keycap)
    
    curved_row = union(*keycaps)
    render_to_file(curved_row, 'tests/output/curved_keycap_row.scad')
    print("已生成弯曲键帽行测试文件")

def run_all_tests():
    """运行所有键帽测试"""
    print("\n=== 运行键帽测试 ===")
    test_simple_keycap()
    test_keycap_row()
    test_curved_keycap_row()
    print("键帽测试完成")

if __name__ == "__main__":
    run_all_tests()