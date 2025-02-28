"""
Compose函数测试 - 展示lib.py中compose函数的使用和与链式调用的对比
"""
import os
import sys

# 添加项目根目录到路径
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.lib import *

# 测试输出目录
TEST_OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '../output')

def test_compose_vs_chain():
    """比较compose函数和链式调用"""
    print("\n=== 测试compose函数与链式调用 ===")
    
    # 创建一个简单的立方体
    base_cube = cube(10, 10, 10)
    
    # 方式1: 链式调用（嵌套结构）
    chain_result = translate(20, 0, 0)(
                    rotate_z(45)(
                        scale(2, 2, 1)(
                            base_cube
                        )
                    )
                  )
    
    # 方式2: compose函数（扁平结构）
    compose_result = compose(
        translate(20, 0, 0),
        rotate_z(45),
        scale(2, 2, 1)
    )(base_cube)
    
    # 输出两种方式生成的模型
    render_to_file(chain_result, os.path.join(TEST_OUTPUT_DIR, 'chain_style.scad'))
    render_to_file(compose_result, os.path.join(TEST_OUTPUT_DIR, 'compose_style.scad'))
    
    print("已生成链式调用和compose函数的比较示例")
    
def test_complex_compose():
    """测试更复杂的compose组合"""
    print("\n=== 测试复杂compose组合 ===")
    
    # 创建一个组合变换
    complex_transform = compose(
        translate(0, 0, 20),    # 第4步: 整体上移
        scale(1, 1, 2),         # 第3步: Z方向拉伸
        rotate_z(30),           # 第2步: 绕Z轴旋转
        rotate_x(45)            # 第1步: 先绕X轴旋转
    )
    
    # 应用到三个不同形状
    shapes = []
    
    # 立方体变换
    cube_shape = complex_transform(cube(10, 10, 10, center=True))
    shapes.append(translate(-20, 0, 0)(colour(200, 100, 100, 1)(cube_shape)))
    
    # 球体变换
    sphere_shape = complex_transform(sphere(6))
    shapes.append(translate(0, 0, 0)(colour(100, 200, 100, 1)(sphere_shape)))
    
    # 圆柱体变换
    cylinder_shape = complex_transform(cylinder(r=5, h=12, center=True))
    shapes.append(translate(20, 0, 0)(colour(100, 100, 200, 1)(cylinder_shape)))
    
    # 组合并渲染
    result = union(*shapes)
    render_to_file(result, os.path.join(TEST_OUTPUT_DIR, 'complex_compose.scad'))
    
    print("已生成复杂compose组合示例")
    
def test_compose_internal():
    """测试compose的内部工作原理"""
    print("\n=== 测试compose内部结构 ===")
    
    # 创建一个compose变换
    my_transform = compose(
        translate(10, 0, 0),
        rotate_z(45),
        scale(2, 2, 2)
    )
    
    # 检查内部结构
    if hasattr(my_transform, 'children'):
        print(f"Composer对象的children长度: {len(my_transform.children)}")
        print(f"children列表内容: {my_transform.children}")
        
    # 应用到一个立方体并渲染
    result = my_transform(cube(5, 5, 5))
    render_to_file(result, os.path.join(TEST_OUTPUT_DIR, 'compose_internal.scad'))
    
    print("已生成compose内部结构测试")

def run_all_tests():
    """运行所有compose相关测试"""
    # 确保测试输出目录存在
    os.makedirs(TEST_OUTPUT_DIR, exist_ok=True)
    
    test_compose_vs_chain()
    test_complex_compose()
    test_compose_internal()
    
    print("Compose函数测试完成")

if __name__ == "__main__":
    run_all_tests()
