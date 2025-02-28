"""
测试运行器 - 集中管理所有测试
方便运行和清理测试生成的文件
"""
import os
import sys
import shutil
import argparse

# 添加项目根目录到路径
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 测试输出目录
TEST_OUTPUT_DIR = os.path.join(os.path.dirname(__file__), 'output')

def ensure_test_output_dir():
    """确保测试输出目录存在"""
    os.makedirs(TEST_OUTPUT_DIR, exist_ok=True)
    
def clean_test_output():
    """清理所有测试输出文件"""
    if os.path.exists(TEST_OUTPUT_DIR):
        print(f"清理测试输出目录: {TEST_OUTPUT_DIR}")
        shutil.rmtree(TEST_OUTPUT_DIR)
        os.makedirs(TEST_OUTPUT_DIR)
        print("清理完成")
    else:
        print("没有测试输出需要清理")

# ========== 测试模块 ==========

def test_basic_shapes():
    """测试基本形状生成"""
    from tests.modules import basic_shapes_test
    ensure_test_output_dir()
    basic_shapes_test.run_all_tests()
    
def test_transformations():
    """测试变换操作"""
    from tests.modules import transformations_test
    ensure_test_output_dir()
    transformations_test.run_all_tests()
    
def test_csg_operations():
    """测试CSG操作"""
    from tests.modules import csg_operations_test
    ensure_test_output_dir()
    csg_operations_test.run_all_tests()

def test_keycap():
    """测试键帽生成"""
    from tests.modules import keycap_test
    ensure_test_output_dir()
    keycap_test.run_all_tests()

def test_chain():
    """测试链式操作"""
    from tests.modules import chain_test
    ensure_test_output_dir()
    chain_test.run_all_tests()

def test_compose():
    """测试compose函数操作"""
    from tests.modules import compose_test
    ensure_test_output_dir()
    compose_test.run_all_tests()

def test_multi_composer():
    """测试多元素Composer结构"""
    from tests.modules import multi_composer_test
    ensure_test_output_dir()
    multi_composer_test.run_all_tests()

# 所有可用的测试
ALL_TESTS = {
    'basic': test_basic_shapes,
    'transform': test_transformations,
    'csg': test_csg_operations,
    'keycap': test_keycap,
    'chain': test_chain,  # 新增的链式操作测试
    'compose': test_compose,  # 新增的compose函数测试
    'multi': test_multi_composer,  # 新增的多元素测试
    'all': None  # 特殊值，表示运行所有测试
}

def list_tests():
    """列出所有可用的测试"""
    print("可用的测试:")
    for name in ALL_TESTS.keys():
        if name != 'all':
            print(f"  - {name}")
    print("  - all (运行所有测试)")

def main():
    """主函数，处理命令行参数"""
    parser = argparse.ArgumentParser(description='Dactyl键盘测试运行器')
    parser.add_argument('--test', '-t', type=str, help='要运行的测试名称')
    parser.add_argument('--list', '-l', action='store_true', help='列出所有可用的测试')
    parser.add_argument('--clean', '-c', action='store_true', help='清理测试输出文件')
    
    args = parser.parse_args()
    
    if args.clean:
        clean_test_output()
        return
        
    if args.list:
        list_tests()
        return
    
    if args.test:
        if args.test == 'all':
            print("运行所有测试...")
            for name, test_func in ALL_TESTS.items():
                if name != 'all' and test_func:
                    print(f"\n--- 运行 {name} 测试 ---")
                    test_func()
        elif args.test in ALL_TESTS and ALL_TESTS[args.test]:
            print(f"运行 {args.test} 测试...")
            ALL_TESTS[args.test]()
        else:
            print(f"错误: 未知的测试名称 '{args.test}'")
            list_tests()
    else:
        # 默认显示帮助
        parser.print_help()

if __name__ == "__main__":
    main()