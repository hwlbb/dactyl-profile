"""
配置系统 - 提供统一的配置管理

该模块扩展了原有的配置类，添加了验证、序列化和计算派生值的功能。
"""
import json
import os
from typing import Dict, Any, List, Optional, Union, Callable


class KeyboardConfig:
    """
    键盘配置类
    
    负责管理所有与键盘布局、尺寸相关的参数。支持从文件加载配置，
    以及计算派生参数。
    """
    
    def __init__(self):
        """初始化默认配置"""
        # 开关基础配置
        self.switch_thickness = 2.0  # 开关厚度
        self.switch_hole_size = 14.4  # 开关安装孔尺寸
        self.switch_width = 14.0  # 开关宽度
        self.switch_height = 14.0  # 开关高度
        self.switch_rim_thickness = 1.5  # 开关边框厚度
        
        # 键盘基础布局
        self.max_rows = 4  # 最大行数
        self.num_cols = 6  # 列数
        self.num_pinky_columns = 2  # 小指区域列数
        self.cols_with_max_rows = [2, 3]  # 拥有最大行数的列
        
        # 键盘角度配置
        self.tenting_angle = 11.0  # 左右倾斜角度（绕Y轴）
        self.back_tilt_angle = 11.0  # 键盘后倾角度（绕X轴）
        self.z_offset = 8.0  # Z轴偏移量
        
        # 支撑结构配置
        self.post_width = 0.5  # 支撑柱宽度
        self.post_rad = 0.25  # 支撑柱半径(post_width/2)
        self.web_thickness = 1.5  # 网格厚度
        
        # SA键帽配置
        self.sa_profile_key_height = 12.7
        self.sa_top_length = 18.25
        self.sa_double_length = 37.5
        
        # 间距配置
        self.extra_width = 2.5  # 列间距
        self.extra_height = 1.0  # 行间距
        self.mount_width = self.switch_width + 3.0  # 安装宽度
        self.mount_height = self.switch_height + 3.0  # 安装高度

        # 底板高度配置
        self.bottom_height = 1.5
        
        # 拇指区域配置
        self.thumb_placements = {
            'right': {'rot': [14, -40, 12], 'move': [-15.4, -9.8, 5.2]},
            'middle': {'rot': [10, -23, 20], 'move': [-33, -15, -6]},
            'left': {'rot': [6, -5, 35], 'move': [-52.8, -25.5, -11.5]},
            'bottom_left': {'rot': [4, -10, 27], 'move': [-33.3, -36.2, -16]},
            'bottom_right': {'rot': [4, -26, 18], 'move': [-13.8, -28.7, -9.6]}
        }
        
        # 拇指区域支柱偏移量
        self.thumb_post_offsets = {
            'bottom_right': {
                'bl': [3, 0, 0],
                'tr': [0, -3.8, 0]
            },
            'right': {
                'bl': [11, 0, 0],
                'tl': [4, 0, 0]
            },
            'bottom_left': {
                'br': [-3, 0, 0],
                'tl': [0, -3, 0]
            },
            'left': {
                'br': [-11.5, 0, 0]
            },
            'middle': {
                'tr': [-2, 0, 0]
            }
        }
        
        # 减重开孔配置
        self.weight_hole_config = {
            'width': 19.5,
            'height': 16.5,
            'z_offset': 0.5,
            'pattern': [
                # 可以添加减重孔的具体模式
            ]
        }
        
        # 计算派生值
        self._calculate_derived_values()
    
    def _calculate_derived_values(self):
        """计算派生值，在配置值更改后自动调用"""
        # 板外宽度
        self.plate_outer_width = self.switch_hole_size + self.switch_rim_thickness * 2
        
        # 键帽总高度
        self.total_key_height = self.switch_thickness + self.sa_profile_key_height
        
        # 列曲率角度（水平方向曲率）
        self.col_curve_angle = 4.0
        
        # 列曲率半径（水平方向曲率）
        self.column_curvature_radius = self.total_key_height + (
            (self.mount_width + self.extra_width) / 2) / self.sin_half_angle(self.col_curve_angle)
        
        # 曲率参考中心
        self.center_col = 3  # 中心列（从0开始，通常是无名指列）
        self.center_row = 1  # 中心行（从0开始，通常是主行）
    
    @staticmethod
    def sin_half_angle(angle_deg):
        """计算半角正弦值"""
        from math import radians, sin
        return sin(radians(angle_deg) / 2)
    
    def row_curve_angle_for_column(self, col):
        """确定每列的行曲率角度（垂直方向曲率）"""
        if col == 1:  # 食指列
            return 20  # 增加弯曲度
        elif col >= self.num_cols - self.num_pinky_columns:  # 小拇指列
            return 22  # 增加弯曲度
        else:
            return 17  # 保持其他列不变
    
    def row_curvature_radius(self, col):
        """计算每列的行曲率半径（垂直方向曲率）"""
        angle = self.row_curve_angle_for_column(col)
        return self.total_key_height + (
            (self.mount_height + self.extra_height) / 2) / self.sin_half_angle(angle)
    
    def column_offset(self, col):
        """计算列的偏移量 [x, y, z]"""
        if col == 2:  # 中指列
            return [0, 7, -3]  # 向后偏移，略降低
        elif col == 3:  # 无名指列
            return [0, 3, -1.5]  # 向后偏移，略降低
        elif col >= self.num_cols - self.num_pinky_columns:  # 小拇指列
            return [1.0, -12.5, 5.0]  # 向右偏移，大幅向前，抬高
        else:  # 大拇指和食指列
            return [0, 0, 0]  # 无偏移
    
    def column_z_rotation(self, col):
        """计算列的Z轴旋转角度（主要用于小拇指区域）"""
        if col >= self.num_cols - self.num_pinky_columns:
            return -3.0
        else:
            return 0
    
    def to_dict(self) -> Dict[str, Any]:
        """
        将配置转换为字典
        
        Returns:
            包含所有配置的字典
        """
        # 过滤掉私有属性和方法
        return {k: v for k, v in self.__dict__.items() if not k.startswith('_')}
    
    def save_to_file(self, filepath: str) -> None:
        """
        将配置保存到文件
        
        Args:
            filepath: 保存路径
        """
        # 确保目录存在
        os.makedirs(os.path.dirname(os.path.abspath(filepath)), exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, ensure_ascii=False, indent=2)
    
    @classmethod
    def load_from_file(cls, filepath: str) -> 'KeyboardConfig':
        """
        从文件加载配置
        
        Args:
            filepath: 配置文件路径
            
        Returns:
            加载的配置对象
        """
        config = cls()
        
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        # 更新配置
        for key, value in data.items():
            if hasattr(config, key):
                setattr(config, key, value)
        
        # 重新计算派生值
        config._calculate_derived_values()
        
        return config
    
    @classmethod
    def create_default(cls) -> 'KeyboardConfig':
        """创建默认配置实例"""
        return cls()


class KeyboardController:
    """
    键盘控制器 - 管理键盘的全局状态和组件交互
    
    替代原有全局变量的中央控制器，提供一致的接口访问键盘配置
    和状态信息。
    """
    
    def __init__(self, config: Optional[KeyboardConfig] = None):
        """
        初始化键盘控制器
        
        Args:
            config: 可选的配置对象，如果不提供则使用默认配置
        """
        self.config = config or KeyboardConfig.create_default()
        self.include_risers = True
        self._components = {}
        
    def register_component(self, name: str, component: Any) -> Any:
        """
        注册一个键盘组件
        
        Args:
            name: 组件名称
            component: 组件对象
            
        Returns:
            注册的组件，便于链式调用
        """
        self._components[name] = component
        return component
        
    def get_component(self, name: str) -> Optional[Any]:
        """
        获取已注册的组件
        
        Args:
            name: 组件名称
            
        Returns:
            组件对象，如果不存在则返回None
        """
        return self._components.get(name)
    
    def set_include_risers(self, value: bool) -> None:
        """
        设置是否包含边框
        
        Args:
            value: 是否包含边框
        """
        self.include_risers = value
        
    def should_include_risers(self) -> bool:
        """
        检查是否应该包含边框
        
        Returns:
            是否应该包含边框
        """
        return self.include_risers
