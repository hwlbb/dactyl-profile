"""
test_core_classes.py - 测试lib核心类结构

这个文件专门演示lib.py中的核心类设计和关系：
1. NativeSCAD - 基础包装类
2. Composer - 组合变换类
3. Merger - 合并操作类
"""
from src.lib import *
import os

def test_nativescad():
    """演示NativeSCAD类的基本功能"""
    print("\n测试NativeSCAD类...")
    
    # 创建基本形状
    base_cube = cube(10, 10, 10)
    print("- 创建了一个10x10x10的立方体")
    
    # 创建基本变换
    moved_cube = translate(20, 0, 0)(base_cube)
    print("- 将立方体沿X轴平移20单位")
    
    # 输出到文件
    output_dir = 'tests/output/core_classes'
    os.makedirs(output_dir, exist_ok=True)
    
    # 同时输出未变换和变换后的对象以便比较
    combined = union(
        base_cube,
        moved_cube
    )
    
    render_to_file(combined, f'{output_dir}/nativescad_demo.scad')
    print(f"- 已保存演示文件: {output_dir}/nativescad_demo.scad")
    
    return combined

def test_composer():
    """演示Composer类的链式调用和组合功能"""
    print("\n测试Composer类...")
    
    # 创建基本形状
    base_cube = cube(10, 10, 10)
    
    # 方法1: 使用链式调用（隐式创建Composer）
    chained = translate(20, 0, 0)(
        rotate_z(45)(
            base_cube
        )
    )
    print("- 使用链式语法: translate(20,0,0)(rotate_z(45)(cube(10,10,10)))")
    
    # 方法2: 使用compose函数（显式创建Composer）
    composed = compose(
        translate(0, 20, 0),
        rotate_z(45)
    )(base_cube)
    print("- 使用compose函数: compose(translate(0,20,0), rotate_z(45))(cube(10,10,10))")
    
    # 展示变换顺序的重要性
    order1 = translate(20, 20, 0)(
        rotate_z(45)(
            base_cube
        )
    )
    print("- 顺序示例1: 先旋转再平移")
    
    order2 = rotate_z(45)(
        translate(20, 20, 0)(
            base_cube
        )
    )
    print("- 顺序示例2: 先平移再旋转")
    
    # 输出到文件
    output_dir = 'tests/output/core_classes'
    os.makedirs(output_dir, exist_ok=True)
    
    # 所有示例合并显示
    all_examples = union(
        base_cube,            # 原始立方体
        chained,              # 链式调用
        composed,             # compose函数
        translate(40, 0, 0)(order1),  # 顺序示例1
        translate(40, 20, 0)(order2)  # 顺序示例2
    )
    
    render_to_file(all_examples, f'{output_dir}/composer_demo.scad')
    print(f"- 已保存演示文件: {output_dir}/composer_demo.scad")
    
    # 也单独保存顺序示例以便比较
    order_compare = union(
        translate(0, 0, 0)(order1),
        translate(30, 0, 0)(order2)
    )
    render_to_file(order_compare, f'{output_dir}/transform_order_compare.scad')
    print(f"- 已保存变换顺序比较: {output_dir}/transform_order_compare.scad")
    
    return all_examples

def test_merger():
    """演示Merger类的布尔操作功能"""
    print("\n测试Merger类...")
    
    # 创建基本形状
    base_cube = cube(10, 10, 10)
    cylinder_shape = translate(5, 5, 0)(cylinder(r=6, h=12))
    sphere_shape = translate(12, 12, 5)(sphere(r=5))
    
    print("- 创建了基础形状: 立方体、圆柱体和球体")
    
    # 测试不同的布尔操作
    union_shape = union(base_cube, cylinder_shape, sphere_shape)
    print("- 使用union()合并三个形状")
    
    difference_shape = difference(base_cube, cylinder_shape)
    print("- 使用difference()从立方体中减去圆柱体")
    
    intersection_shape = intersection(base_cube, cylinder_shape)
    print("- 使用intersection()获取立方体和圆柱体的交集")
    
    hull_shape = hull(base_cube, sphere_shape)
    print("- 使用hull()创建立方体和球体的凸包")
    
    # 输出到文件
    output_dir = 'tests/output/core_classes'
    os.makedirs(output_dir, exist_ok=True)
    
    # 保存每种操作的示例
    operations = {
        'union': union_shape,
        'difference': difference_shape, 
        'intersection': intersection_shape,
        'hull': hull_shape
    }
    
    for op_name, shape in operations.items():
        render_to_file(shape, f'{output_dir}/merger_{op_name}_demo.scad')
        print(f"- 已保存{op_name}操作示例: {output_dir}/merger_{op_name}_demo.scad")
    
    # 并排显示所有操作结果
    display = union(
        union_shape,
        translate(20, 0, 0)(difference_shape),
        translate(0, 20, 0)(intersection_shape),
        translate(20, 20, 0)(hull_shape)
    )
    
    render_to_file(display, f'{output_dir}/merger_all_demo.scad')
    print(f"- 已保存所有操作组合视图: {output_dir}/merger_all_demo.scad")
    
    return display

def main():
    """运行所有核心类测试"""
    print("开始测试lib.py核心类...")
    
    # 创建输出目录
    output_dir = 'tests/output/core_classes'
    os.makedirs(output_dir, exist_ok=True)
    
    # 测试各个核心类
    test_nativescad()
    test_composer()
    test_merger()
    
    # 综合演示 - 展示三个类如何协同工作
    print("\n创建综合演示...")
    
    # 基础形状 (NativeSCAD)
    base_cube = cube(8, 8, 4)
    base_cylinder = cylinder(r=4, h=10)
    
    # 变换组合 (Composer)
    transformed_cube = translate(0, 0, 5)(
        rotate_z(45)(
            colour(255, 0, 0, 1)(base_cube)
        )
    )
    
    transformed_cylinder = translate(12, 0, 0)(
        base_cylinder
    )
    
    # 布尔操作 (Merger)
    final_shape = union(
        transformed_cube,
        difference(
            transformed_cylinder,
            translate(12, 0, 5)(sphere(r=3))
        )
    )
    
    # 输出最终结果
    render_to_file(final_shape, f'{output_dir}/combined_demo.scad')
    print(f"- 已保存综合演示: {output_dir}/combined_demo.scad")
    
    print("\n所有核心类测试完成!")

if __name__ == "__main__":
    main()