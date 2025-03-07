"""
外壳构建 - 处理键盘外壳和底板的构建
注意：这个文件现在只是转发到新的模块结构，为了保持向后兼容
"""
# 从新模块导入所有功能
from .case import (
    right_shell, left_shell, bottom_plate, left_bottom_plate
)

# 导出这些函数，保持向后兼容
__all__ = ['right_shell', 'left_shell', 'bottom_plate', 'left_bottom_plate']