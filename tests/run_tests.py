"""
运行所有单元测试并生成覆盖率报告
"""
import unittest
import sys
import os
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# 尝试导入 coverage
try:
    import coverage
    COVERAGE_AVAILABLE = True
except ImportError:
    COVERAGE_AVAILABLE = False
    print("警告: coverage 未安装，无法生成覆盖率报告")
    print("安装命令: pip install coverage")


def discover_and_run_tests():
    """发现并运行所有测试"""
    # 发现测试
    loader = unittest.TestLoader()
    start_dir = os.path.dirname(__file__)
    suite = loader.discover(start_dir, pattern='test_*.py')
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result


def run_tests_with_coverage():
    """使用 coverage 运行测试"""
    if not COVERAGE_AVAILABLE:
        return discover_and_run_tests()
    
    # 创建 coverage 对象
    cov = coverage.Coverage(
        source=[str(project_root / "src")],
        omit=[
            "*/tests/*",
            "*/test_*.py",
            "*/__pycache__/*"
        ]
    )
    
    cov.start()
    
    # 运行测试
    result = discover_and_run_tests()
    
    cov.stop()
    cov.save()
    
    # 生成报告
    print("\n" + "="*80)
    print("生成覆盖率报告...")
    print("="*80)
    
    # 控制台报告
    cov.report()
    
    # HTML 报告
    html_dir = project_root / "htmlcov"
    cov.html_report(directory=str(html_dir))
    print(f"\nHTML 覆盖率报告已生成到: {html_dir}/index.html")
    
    return result


def main():
    """主函数"""
    print("="*80)
    print("LanguageMentor 单元测试")
    print("="*80)
    
    if COVERAGE_AVAILABLE:
        result = run_tests_with_coverage()
    else:
        result = discover_and_run_tests()
    
    # 总结
    print("\n" + "="*80)
    print("测试总结")
    print("="*80)
    print(f"运行测试: {result.testsRun}")
    print(f"成功: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"失败: {len(result.failures)}")
    print(f"错误: {len(result.errors)}")
    
    if result.failures:
        print("\n失败的测试:")
        for test, traceback in result.failures:
            print(f"  - {test}: {traceback[:200]}...")
    
    if result.errors:
        print("\n错误的测试:")
        for test, traceback in result.errors:
            print(f"  - {test}: {traceback[:200]}...")
    
    # 退出码
    exit_code = 0 if result.wasSuccessful() else 1
    sys.exit(exit_code)


if __name__ == '__main__':
    main()

