class KeyboardConfig:
    """键盘配置"""
    def __init__(self):
        # 开关配置
        self.switch_size = 14.4  # 开关外壳的大小
        self.switch_height = 14.0  # 开关外壳的高度
        self.rim_thickness = 1.5  # 开关外壳的壁厚

        # 稳定器配置
        self.stabilizer_width = 6.65  # 稳定器的宽度
        self.stabilizer_depth = 13.5  # 稳定器的深度
        self.stabilizer_distance = 23.8  # 稳定器两边的距离

        # 键盘配置
        self.tenting_angle = 11.0  # 倾斜角度
        self.keyboard_y_rotation = 8.0  # Y轴旋转角度
        self.num_rows = 4  # 行数
        self.num_cols = 6  # 列数

        # 键帽配置
        self.keycap_top_length = 18.0  # 键帽顶部长度
        self.keycap_bottom_length = 18.0  # 键帽底部长度
        self.keycap_height = 10.0  # 键帽高度
        self.keycap_top_height = 0.5  # 键帽顶部厚度

    @classmethod
    def create_default(cls):
        """创建默认配置"""
        return cls() 