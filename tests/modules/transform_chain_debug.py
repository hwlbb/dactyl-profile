"""
变换链和compose调试 - 详细展示内部工作机制
"""
import os
import sys

# 添加项目根目录到路径
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.lib import *

def test_chain_operations():
    """测试不同情况下的变换链构建过程"""
    print("\n===== 测试1: 简单链式调用 =====")
    # 创建一个基本形状
    base_cube = cube(5, 5, 5)
    print(f"基本形状: {type(base_cube).__name__}")
    
    # 应用单个变换
    simple_transform = translate(10, 0, 0)(base_cube)
    print(f"应用单个变换后的对象类型: {type(simple_transform).__name__}")
    print(f"变换链长度: {len(simple_transform.objects)}")
    print(f"变换链成员: {[type(obj).__name__ for obj in simple_transform.objects]}")
    
    # 应用多级链式变换
    chain_transform = translate(10, 0, 0)(rotate_z(45)(scale(2, 2, 1)(base_cube)))
    print("\n===== 测试2: 多级链式调用 =====")
    print(f"多级变换链类型: {type(chain_transform).__name__}")
    print(f"最外层变换链长度: {len(chain_transform.objects)}")
    print(f"最外层变换链成员: {[type(obj).__name__ for obj in chain_transform.objects]}")
    
    # 第二层变换链
    second_layer = chain_transform.objects[1]
    if isinstance(second_layer, TransformChain):
        print(f"第二层变换链长度: {len(second_layer.objects)}")
        print(f"第二层变换链成员: {[type(obj).__name__ for obj in second_layer.objects]}")
        
        # 第三层变换链
        third_layer = second_layer.objects[1]
        if isinstance(third_layer, TransformChain):
            print(f"第三层变换链长度: {len(third_layer.objects)}")
            print(f"第三层变换链成员: {[type(obj).__name__ for obj in third_layer.objects]}")
    
    # 测试compose
    print("\n===== 测试3: compose函数 =====")
    composed = compose(translate(10, 0, 0), rotate_z(45), scale(2, 2, 1))
    print(f"compose结果类型: {type(composed).__name__}")
    print(f"compose变换链长度: {len(composed.objects)}")
    print(f"compose变换链成员: {[type(obj).__name__ for obj in composed.objects]}")
    
    # 应用compose到形状
    composed_result = composed(base_cube)
    print(f"compose应用后类型: {type(composed_result).__name__}")
    print(f"compose应用后链长度: {len(composed_result.objects)}")
    print(f"compose应用后链成员: {[type(obj).__name__ for obj in composed_result.objects]}")

if __name__ == "__main__":
    test_chain_operations()
