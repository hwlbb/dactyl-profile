"""
Dactyl键盘生成器 - 主程序入口(重构版)
功能：生成人体工学分离式机械键盘的3D模型
基于新的场景图架构设计
"""
import os
from .core.scene import Scene
from .core.config import KeyboardConfig
from .components.keycap import SAKeycapComponent
from .components.switch import SwitchComponent, FilledSwitchComponent

def render_component_demos():
    """渲染当前实现的组件演示"""
    print("生成组件演示...")
    
    # 确保输出目录存在
    os.makedirs('output/new', exist_ok=True)
    
    # 创建配置
    config = KeyboardConfig.create_default()
    
    # 渲染SA键帽
    keycap_scene = Scene(name="keycap_demo")
    sa_keycap = SAKeycapComponent(config)
    sa_keycap.create_node(keycap_scene, name="sa_keycap")
    keycap_scene.render_to_file('output/new/sa_keycap.scad')
    print("- 已生成SA键帽演示: output/new/sa_keycap.scad")
    
    # 渲染开关
    switch_scene = Scene(name="switch_demo")
    switch = SwitchComponent(config)
    switch.create_node(switch_scene, name="switch")
    switch_scene.render_to_file('output/new/switch.scad')
    print("- 已生成开关演示: output/new/switch.scad")
    
    # 渲染填充开关
    filled_switch_scene = Scene(name="filled_switch_demo")
    filled_switch = FilledSwitchComponent(config)
    filled_switch.create_node(filled_switch_scene, name="filled_switch")
    filled_switch_scene.render_to_file('output/new/filled_switch.scad')
    print("- 已生成填充开关演示: output/new/filled_switch.scad")
    
    # 渲染开关+键帽组合
    combo_scene = Scene(name="switch_keycap_combo")
    
    # 添加开关
    switch = SwitchComponent(config)
    switch_node = switch.create_node(combo_scene, "switch")
    
    # 添加键帽
    keycap = SAKeycapComponent(config)
    keycap_node = keycap.create_node(name="keycap")
    combo_scene.add(keycap_node)
    
    combo_scene.render_to_file('output/new/switch_keycap_combo.scad')
    print("- 已生成开关+键帽组合演示: output/new/switch_keycap_combo.scad")

def run():
    """
    生成所有需要的键盘模型文件
    这是重构后的主入口函数
    """
    print('开始生成键盘3D模型(新架构)...')
    
    # 渲染组件演示
    render_component_demos()
    
    # 当前版本只渲染演示组件
    # 随着更多组件被实现，这里将添加完整键盘的渲染代码
    
    print('所有模型已成功生成!')

if __name__ == "__main__":
    run()
