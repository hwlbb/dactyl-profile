"""
键盘外壳模块 - 整合所有外壳组件
"""
from .assembly import right_shell, left_shell, bottom_plate, left_bottom_plate

# 导出主要函数，保持向后兼容
__all__ = ['right_shell', 'left_shell', 'bottom_plate', 'left_bottom_plate']
