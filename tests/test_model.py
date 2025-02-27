"""
test_model.py - 测试模型生成示例
这个文件展示了如何使用lib库生成简单的测试模型
"""
from src.lib import *  # 导入所有3D操作函数
import os

def simple_key():
    """创建一个简单的按键测试模型"""
    # 创建按键底座
    base = translate(0, 0, 0)(
        cube(18, 18, 4)  # 18mm x 18mm 的正方形，高4mm
    )
    
    # 创建按键帽
    cap_bottom = translate(1, 1, 4)(
        cube(16, 16, 1)  # 略小于底座的顶面
    )
    
    cap_top = translate(3, 3, 5)(
        cube(12, 12, 2)  # 更小的顶面
    )
    
    # 合并底座和按键帽为完整按键
    key = union(
        base,
        cap_bottom,
        cap_top
    )
    
    # 添加开关孔
    switch_hole = translate(6, 6, -1)(
        cylinder(r=5.5, h=6)  # 中间开孔
    )
    
    # 从按键中减去开关孔
    return difference(key, switch_hole)

def tented_keyboard_base():
    """创建一个简单的倾斜键盘底座"""
    # 创建主体
    main_body = translate(-40, -30, 0)(
        cube(80, 60, 10)
    )
    
    # 添加倾斜效果
    tented = rotate_x(15)(  # 15度倾斜角
        main_body
    )
    
    # 创建底座支撑
    support = translate(-20, 0, 0)(
        cube(40, 20, 20)
    )
    
    return union(tented, support)

def thumb_cluster():
    """创建一个简单的拇指区域模型"""
    thumb1 = translate(-25, 10, 12)(
        rotate_y(-20)(
            rotate_z(30)(
                simple_key()
            )
        )
    )
    
    thumb2 = translate(-15, 25, 8)(
        rotate_y(-15)(
            rotate_z(45)(
                simple_key()
            )
        )
    )
    
    return union(thumb1, thumb2)

def test_model():
    """创建完整的测试模型"""
    # 基础键盘
    base = tented_keyboard_base()
    
    # 添加一些按键
    keys = []
    for row in range(3):
        for col in range(5):
            key = translate(col * 20 - 30, row * 20 - 20, 10)(
                simple_key()
            )
            keys.append(key)
    
    # 添加拇指区域
    thumb = thumb_cluster()
    
    # 合并所有部分
    full_model = union(
        base,
        *keys,
        thumb
    )
    
    return full_model

def main():
    """生成测试模型SCAD文件"""
    # 创建输出目录
    output_dir = 'tests/output'
    os.makedirs(output_dir, exist_ok=True)
    
    print("正在生成测试模型...")
    
    # 生成单个按键
    render_to_file(simple_key(), f'{output_dir}/test_key.scad')
    print(f"- 已生成按键测试模型: {output_dir}/test_key.scad")
    
    # 生成键盘底座
    render_to_file(tented_keyboard_base(), f'{output_dir}/test_base.scad')
    print(f"- 已生成底座测试模型: {output_dir}/test_base.scad")
    
    # 生成拇指区域
    render_to_file(thumb_cluster(), f'{output_dir}/test_thumb.scad')
    print(f"- 已生成拇指区域测试模型: {output_dir}/test_thumb.scad")
    
    # 生成完整模型
    render_to_file(test_model(), f'{output_dir}/test_full.scad')
    print(f"- 已生成完整测试模型: {output_dir}/test_full.scad")
    
    print("所有测试模型生成完成!")

if __name__ == "__main__":
    main()