from ..core.primitives import cube
from ..core.combine import union, difference
from ..config import KeyboardConfig

class KeySwitch:
    """键盘开关类"""
    def __init__(self, config: KeyboardConfig):
        self.config = config

    def create(self):
        """创建开关外壳"""
        # 外壳
        outer = cube(
            [
                self.config.switch_size + self.config.rim_thickness * 2,
                self.config.switch_size + self.config.rim_thickness * 2,
                self.config.switch_height
            ]
        )

        # 内部空间
        inner = cube(
            [
                self.config.switch_size,
                self.config.switch_size,
                self.config.switch_height
            ]
        ).translate(
            self.config.rim_thickness,
            self.config.rim_thickness,
            0
        )

        # 从外壳中减去内部空间
        return difference(outer, inner)

    def create_with_stabilizer(self):
        """创建带稳定器的开关外壳"""
        # 基础开关
        switch = self.create()

        # 稳定器左右两边的空间
        stab_left = cube(
            [
                self.config.stabilizer_width,
                self.config.stabilizer_depth,
                self.config.switch_height
            ]
        ).translate(
            -(self.config.stabilizer_distance + self.config.stabilizer_width) / 2,
            (self.config.switch_size - self.config.stabilizer_depth) / 2,
            0
        )

        stab_right = cube(
            [
                self.config.stabilizer_width,
                self.config.stabilizer_depth,
                self.config.switch_height
            ]
        ).translate(
            (self.config.stabilizer_distance - self.config.stabilizer_width) / 2,
            (self.config.switch_size - self.config.stabilizer_depth) / 2,
            0
        )

        # 合并所有部分
        return union(switch, stab_left, stab_right) 