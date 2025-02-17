import os
import pytest
from src.core import cube, sphere, union, difference
from src.components import KeySwitch
from src.config import KeyboardConfig
from solid import scad_render_to_file

# 输出目录
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), 'output')

@pytest.fixture(scope="session", autouse=True)
def setup_output_dir():
    """确保输出目录存在"""
    os.makedirs(OUTPUT_DIR, exist_ok=True)

def output_path(filename):
    """生成输出文件的完整路径"""
    return os.path.join(OUTPUT_DIR, filename)

def test_basic_shapes():
    """测试基本形状和变换"""
    # 创建一个立方体并应用变换
    base = cube(10)\
        .translate(0, 0, 5)\
        .rotate_x(45)
    
    # 创建一个球体并移动位置
    sphere_shape = sphere(3)\
        .translate(5, 5, 5)
    
    # 合并两个形状
    result = union(base, sphere_shape)
    
    # 保存结果
    scad_render_to_file(result.build(), output_path('test_basic.scad'))
    
    # 验证结果
    assert os.path.exists(output_path('test_basic.scad'))

def test_switch():
    """测试开关组件"""
    # 创建配置
    config = KeyboardConfig.create_default()
    
    # 创建普通开关
    switch = KeySwitch(config).create()
    scad_render_to_file(switch.build(), output_path('test_switch.scad'))
    
    # 创建带稳定器的开关
    switch_with_stab = KeySwitch(config).create_with_stabilizer()
    scad_render_to_file(switch_with_stab.build(), output_path('test_switch_with_stab.scad'))
    
    # 验证结果
    assert os.path.exists(output_path('test_switch.scad'))
    assert os.path.exists(output_path('test_switch_with_stab.scad')) 