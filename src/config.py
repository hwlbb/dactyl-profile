class KeyboardConfig:
    """键盘基础配置"""
    def __init__(self):
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
        self.tenting_angle = 11.0  # 左右倾斜角度
        self.keyboard_y_rotation = 8.0  # 键盘后倾角度
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

    @classmethod
    def create_default(cls):
        """创建默认配置实例"""
        return cls()