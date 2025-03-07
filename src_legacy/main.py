"""
Dactyl 键盘生成器 - 主程序入口
功能：生成人体工学分离式机械键盘的3D模型
"""
from .lib import render_to_file
# 修改导入路径，直接从case模块导入
from .case import right_shell, left_shell, bottom_plate, left_bottom_plate

def run():
    """生成所有需要的键盘模型文件"""
    print('开始生成键盘3D模型(旧架构)...')
    
    # 确保legacy输出目录存在
    import os
    os.makedirs('output/legacy', exist_ok=True)
    
    # 生成右手部分
    render_to_file(right_shell(), 'output/legacy/right.scad')
    print('- 已生成右侧键盘壳体: output/legacy/right.scad')
    
    # 生成左手部分
    render_to_file(left_shell(), 'output/legacy/left.scad')
    print('- 已生成左侧键盘壳体: output/legacy/left.scad')
    
    # 生成右底板
    render_to_file(bottom_plate(), 'output/legacy/right_bottom_plate.scad')
    print('- 已生成右侧底板: output/legacy/right_bottom_plate.scad')
    
    # 生成左底板
    render_to_file(left_bottom_plate(), 'output/legacy/left_bottom_plate.scad')
    print('- 已生成左侧底板: output/legacy/left_bottom_plate.scad')
    
    print('所有模型已成功生成!')

if __name__ == '__main__':
    run()
