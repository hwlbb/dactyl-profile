"""
Dactyl 键盘生成器 - 主程序入口
功能：生成人体工学分离式机械键盘的3D模型
"""
from .lib import render_to_file
from .case_utils import right_shell, left_shell, bottom_plate, left_bottom_plate

def run():
    """生成所有需要的键盘模型文件"""
    print('开始生成键盘3D模型...')
    
    # 生成右手部分
    render_to_file(right_shell(), 'output/right.scad')
    print('- 已生成右侧键盘壳体: output/right.scad')
    
    # 生成左手部分
    render_to_file(left_shell(), 'output/left.scad')
    print('- 已生成左侧键盘壳体: output/left.scad')
    
    # 生成右底板
    render_to_file(bottom_plate(), 'output/right_bottom_plate.scad')
    print('- 已生成右侧底板: output/right_bottom_plate.scad')
    
    # 生成左底板
    render_to_file(left_bottom_plate(), 'output/left_bottom_plate.scad')
    print('- 已生成左侧底板: output/left_bottom_plate.scad')
    
    print('所有模型已成功生成!')

if __name__ == '__main__':
    run()
