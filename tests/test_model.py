"""
test_model.py - 测试模型生成示例
这个文件展示了如何使用lib库生成简单的测试模型
"""
from src.lib import *  # 导入所有3D操作函数
import os

# 函数式链式调用演示
def demo_chain():
    """演示lib库的链式调用特性"""
    print("创建链式调用演示...")
    
    # 创建一个简单的立方体
    basic_cube = cube(10, 10, 10)
    
    # 使用链式调用进行变换
    transformed_cube = translate(15, 0, 0)(
        rotate_z(45)(
            colour(255, 0, 0, 1)(  # 红色立方体
                basic_cube
            )
        )
    )
    
    # 创建第二个物体
    sphere_obj = translate(-15, 0, 0)(
        sphere(r=6)
    )
    
    # 合并两个物体
    result = union(transformed_cube, sphere_obj)
    
    # 输出到文件
    output_dir = 'tests/output'
    os.makedirs(output_dir, exist_ok=True)
    render_to_file(result, f'{output_dir}/chain_demo.scad')
    print(f"- 已生成链式调用演示: {output_dir}/chain_demo.scad")
    
    return result

# CSG操作演示
def demo_csg_operations():
    """演示构造立体几何(CSG)操作"""
    print("创建CSG操作演示...")
    
    # 基础形状
    base_cube = translate(0, 0, 0)(cube(20, 20, 5))
    small_cube = translate(5, 5, 0)(cube(10, 10, 10))
    top_cylinder = translate(10, 10, 0)(cylinder(r=8, h=15))
    side_sphere = translate(0, 10, 10)(sphere(r=7))
    
    # 1. 联合操作(union) - 合并多个对象
    union_result = union(base_cube, top_cylinder)
    
    # 2. 差集操作(difference) - 从第一个对象减去其他对象
    diff_result = difference(base_cube, top_cylinder)
    
    # 3. 交集操作(intersection) - 只保留共同区域
    intersect_result = intersection(base_cube, top_cylinder)
    
    # 4. 外壳操作(hull) - 创建包含所有对象的凸包
    hull_result = hull(small_cube, side_sphere)
    
    # 布局所有结果用于展示
    results = [
        translate(-30, 20, 0)(union_result),           # 联合
        translate(30, 20, 0)(diff_result),            # 差集
        translate(-30, -20, 0)(intersect_result),     # 交集
        translate(30, -20, 0)(hull_result),           # 凸包
    ]
    
    # 输出到文件
    output_dir = 'tests/output'
    os.makedirs(output_dir, exist_ok=True)
    
    # 合并为一个场景来显示所有操作
    all_results = union(*results)
    render_to_file(all_results, f'{output_dir}/csg_operations.scad')
    print(f"- 已生成CSG操作演示: {output_dir}/csg_operations.scad")
    
    # 也分别输出每个操作以便单独查看
    csg_types = ['union', 'difference', 'intersection', 'hull']
    operations = [union_result, diff_result, intersect_result, hull_result]
    
    for type_name, operation in zip(csg_types, operations):
        render_to_file(operation, f'{output_dir}/csg_{type_name}.scad')
        print(f"- 已生成{type_name}操作示例: {output_dir}/csg_{type_name}.scad")
    
    return all_results

# 基本变换演示
def demo_transformations():
    """演示基本的3D变换操作"""
    print("创建变换操作演示...")
    
    # 创建基础形状 - 带有色彩标记方向的立方体
    def direction_cube():
        # 基础立方体
        base = cube(10, 10, 10)
        
        # 在X轴添加红色标记
        x_marker = translate(10, 5, 5)(
            colour(255, 0, 0, 1)(  # 红色
                cylinder(r=1, h=5)
            )
        )
        
        # 在Y轴添加绿色标记
        y_marker = translate(5, 10, 5)(
            colour(0, 255, 0, 1)(  # 绿色
                rotate_x(90)(
                    cylinder(r=1, h=5)
                )
            )
        )
        
        # 在Z轴添加蓝色标记
        z_marker = translate(5, 5, 10)(
            colour(0, 0, 255, 1)(  # 蓝色
                rotate_y(90)(
                    cylinder(r=1, h=5)
                )
            )
        )
        
        return union(base, x_marker, y_marker, z_marker)
    
    # 创建标记方向的立方体
    base_cube = direction_cube()
    
    # 1. 平移变换
    translated = translate(20, 0, 0)(base_cube)
    
    # 2. X轴旋转
    rotated_x = translate(-20, 0, 0)(
        rotate_x(45)(base_cube)
    )
    
    # 3. Y轴旋转
    rotated_y = translate(0, 20, 0)(
        rotate_y(45)(base_cube)
    )
    
    # 4. Z轴旋转
    rotated_z = translate(0, -20, 0)(
        rotate_z(45)(base_cube)
    )
    
    # 5. 复合变换 (组合多个变换)
    compound = translate(20, 20, 0)(
        rotate_z(30)(
            rotate_y(30)(
                rotate_x(30)(base_cube)
            )
        )
    )
    
    # 6. 使用compose函数组合变换
    using_compose = translate(-20, -20, 0)(
        compose(
            rotate_z(30),
            rotate_y(30),
            rotate_x(30)
        )(base_cube)
    )
    
    # 7. 缩放变换
    scaled = translate(20, -20, 0)(
        scale(1.5, 0.8, 1.2)(base_cube)
    )
    
    # 8. 镜像变换
    mirrored = translate(-20, 20, 0)(
        mirror(1, 0, 0)(base_cube)  # X轴镜像
    )
    
    # 组合所有示例
    all_transformations = union(
        base_cube,          # 原始形状
        translated,         # 平移
        rotated_x,          # X轴旋转
        rotated_y,          # Y轴旋转
        rotated_z,          # Z轴旋转
        compound,           # 复合变换
        using_compose,      # 使用compose函数
        scaled,             # 缩放
        mirrored            # 镜像
    )
    
    # 输出到文件
    output_dir = 'tests/output'
    os.makedirs(output_dir, exist_ok=True)
    render_to_file(all_transformations, f'{output_dir}/transformations.scad')
    print(f"- 已生成变换操作演示: {output_dir}/transformations.scad")
    
    return all_transformations

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
    
    # 添加链式调用演示
    demo_chain()
    
    # 添加CSG操作演示
    demo_csg_operations()
    
    # 添加变换操作演示
    demo_transformations()
    
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