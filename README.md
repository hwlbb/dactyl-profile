# Dactyl-Profile 键盘生成器

这是一个用于生成Dactyl系列人体工程学分离式机械键盘3D模型的工具。该项目通过参数化设计，允许用户自定义键盘的几何形状和布局。

## 项目重构

此项目正在进行全面重构，目标是提高代码可维护性、可扩展性和可读性。

### 重构目标

- 创建统一的变换系统
- 采用基于场景图的架构
- 解耦组件之间的依赖
- 消除全局状态
- 为未来的JavaScript迁移做准备

### 重构进度

1. **阶段1：核心架构** [已完成]
   - ✅ 创建统一的变换系统 (`src/core/transform.py`)
   - ✅ 实现场景图架构 (`src/core/scene.py`)
   - ✅ 设计配置系统 (`src/core/config.py`)

2. **阶段2：几何系统** [已完成]
   - ✅ 实现基础形状 (`src/geometry/primitives.py`)
   - ✅ 构建布尔操作系统 (`src/geometry/operations.py`)
   - ✅ 创建参数化形状库

3. **阶段3：组件迁移** [进行中]
   - ✅ 实现组件基类 (`src/components/base.py`)
   - ✅ 迁移开关组件 (`src/components/switch.py`)
   - ✅ 迁移键帽组件 (`src/components/keycap.py`)
   - ⬜ 重构拇指区域
   - ⬜ 重构支撑系统

4. **阶段4：外壳和测试** [未开始]
   - ⬜ 迁移外壳系统
   - ⬜ 实现比较测试
   - ⬜ 优化性能

## 项目结构

