#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+ #
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+ #
import os
import re
import subprocess
import sys
import tempfile
import shutil
import fire
import ast
import datetime

# 忽略文件配置表（使用正则表达式）
IGNORE_FILES = [
    r'\.pyc$',           # Python 编译文件
    r'\.pyo$',           # Python 优化文件
    r'_ui\.py$',         # Qt Designer 生成的 UI 文件
    r'_rc\.py$',         # Qt 资源编译文件
    r'_rc2py\.py$',      # Qt 资源转换文件
    r'^test_.*\.py$',    # 测试文件（前缀）
    r'.*_test\.py$',     # 测试文件（后缀）
    r'.*builder\.py$',   # 构建器文件
    r'.*build\.py$',     # 构建脚本
    r'.*package\.py$',   # 打包脚本
    r".*_script\.py$",   # 脚本文件
    r"^resources\.py$",  # 资源文件
]

# 忽略文件夹配置表（使用正则表达式）
IGNORE_DIRS = [
    r'^build$',          # 构建输出目录
    r'^dist$',           # 分发目录
    r'^__pycache__$',    # Python 字节码缓存
    r'^\.git$',          # Git 版本控制
    r'^temp$',           # 临时目录
    r'^tmp$',            # 临时目录
    r'^\.idea$',         # PyCharm IDE 配置
    r'^\.vscode$',       # VS Code IDE 配置
    r'^packages$',       # 包目录
    r'^pip_packages$',   # pip 包目录
    r"^file$",           # 文件目录
    r"^fix$",            # 修复目录
    r"^icon$",           # 图标目录
    r".*del$",           # 删除目录
    r".*exe$",           # 可执行文件目录
    r"^site-packages$",  # Python 站点包
    r"^third-party$",    # 第三方库目录
    r"^plug-ins$",       # 插件目录
    r"^icons$",          # 图标目录
    r"^other$",          # 其他目录
    r"^__pycache__$",    # Python 缓存（重复）
    r".*zip$"            # 压缩包目录
]


# +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+ #
def build_ignore_patterns():
    """构建正则表达式模式列表"""
    ignore_file_patterns = [re.compile(pattern) for pattern in IGNORE_FILES]
    ignore_dir_patterns = [re.compile(pattern) for pattern in IGNORE_DIRS]
    return ignore_file_patterns, ignore_dir_patterns


def should_ignore_file(file_path, ignore_file_patterns):
    """
    使用正则表达式判断文件是否应该被忽略

    Args:
        file_path: 文件路径
        ignore_file_patterns: 忽略文件的正则表达式模式列表

    Returns:
        True 如果文件应该被忽略
    """
    filename = os.path.basename(file_path)
    for pattern in ignore_file_patterns:
        if pattern.search(filename):
            return True
    return False


def should_ignore_dir(dir_path, ignore_dir_patterns):
    """
    使用正则表达式判断目录是否应该被忽略

    Args:
        dir_path: 目录路径
        ignore_dir_patterns: 忽略目录的正则表达式模式列表

    Returns:
        True 如果目录应该被忽略
    """
    dirname = os.path.basename(dir_path)
    for pattern in ignore_dir_patterns:
        if pattern.search(dirname):
            return True
    return False


def scan_python_files(source_dir, ignore_file_patterns, ignore_dir_patterns):
    """
    扫描目录，获取所有非忽略的 Python 文件

    Args:
        source_dir: 源目录路径
        ignore_file_patterns: 忽略文件的正则表达式模式列表
        ignore_dir_patterns: 忽略目录的正则表达式模式列表

    Returns:
        list: Python 文件路径列表
    """
    python_files = []

    # 遍历目录树
    for root, dirs, files in os.walk(source_dir):
        # 过滤忽略的目录（原地修改 dirs，避免递归进入被忽略的目录）
        dirs[:] = [d for d in dirs if not should_ignore_dir(os.path.join(root, d), ignore_dir_patterns)]

        # 查找 Python 文件
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                if not should_ignore_file(file_path, ignore_file_patterns):
                    python_files.append(file_path)

    return python_files


def copy_filtered_files(source_dir, temp_dir, ignore_file_patterns, ignore_dir_patterns):
    """
    复制过滤后的文件到临时目录，保持目录结构

    Args:
        source_dir: 源目录路径
        temp_dir: 临时目录路径
        ignore_file_patterns: 忽略文件的正则表达式模式列表
        ignore_dir_patterns: 忽略目录的正则表达式模式列表
    """
    # 遍历源目录
    for root, dirs, files in os.walk(source_dir):
        # 过滤忽略的目录（原地修改 dirs，避免递归进入被忽略的目录）
        dirs[:] = [d for d in dirs if not should_ignore_dir(os.path.join(root, d), ignore_dir_patterns)]

        # 计算相对路径
        rel_path = os.path.relpath(root, source_dir)

        # 创建目标目录
        if rel_path == '.':
            target_dir = temp_dir
        else:
            target_dir = os.path.join(temp_dir, rel_path)
            os.makedirs(target_dir, exist_ok=True)

        # 复制未被忽略的 Python 文件
        for file in files:
            file_path = os.path.join(root, file)
            if file.endswith('.py') and not should_ignore_file(file_path, ignore_file_patterns):
                shutil.copy2(file_path, target_dir)


def run_pipreqs(temp_dir, output_file):
    """
    运行 pipreqs 收集依赖

    Args:
        temp_dir: 临时目录路径（包含过滤后的 Python 文件）
        output_file: 输出的 requirements.txt 文件路径

    Returns:
        tuple: (是否成功, 是否生成了文件)
    """
    # 构建命令：使用 UTF-8 编码，强制覆盖，指定输出文件路径
    cmd = ['pipreqs', '--encoding=utf8', '--force', temp_dir, '--savepath', output_file]

    try:
        # 执行 pipreqs 命令（不使用 check=True，允许有 WARNING 但仍然生成文件）
        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')

        # 打印 pipreqs 的输出信息（包含 WARNING 和 INFO）
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr)

        # 检查是否生成了文件
        success = os.path.exists(output_file)
        return True, success

    except FileNotFoundError:
        print("=" * 80)
        print("错误: 未找到 pipreqs 命令！")
        print("请确保 pipreqs.exe 在 PATH 环境变量中")
        print("安装命令: pip install pipreqs")
        print("=" * 80)
        return False, False


def parse_requirements_file(file_path):
    """
    解析 requirements.txt 文件，返回包名列表

    Args:
        file_path: requirements.txt 文件路径

    Returns:
        list: 包名列表（无版本号）
    """
    packages = []
    if not os.path.exists(file_path):
        return packages

    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            # 跳过空行和注释
            if not line or line.startswith('#'):
                continue
            # 提取包名（去掉版本号）
            package_name = line.split('==')[0].split('>=')[0].split('<=')[0].split('~=')[0].split('<')[0].split('>')[0].strip()
            if package_name:
                packages.append(package_name)

    return packages


def extract_all_imports(source_dir, ignore_file_patterns, ignore_dir_patterns):
    """
    从所有 Python 文件中提取导入的第三方包

    Args:
        source_dir: 源目录路径
        ignore_file_patterns: 忽略文件的正则表达式模式列表
        ignore_dir_patterns: 忽略目录的正则表达式模式列表

    Returns:
        set: 第三方包名集合
    """
    all_imports = set()

    # 动态获取当前 Python 版本的标准库列表
    STANDARD_LIBRARIES = getattr(sys, 'stdlib_module_names', set())

    for root, dirs, files in os.walk(source_dir):
        # 过滤忽略的目录
        dirs[:] = [d for d in dirs if not should_ignore_dir(os.path.join(root, d), ignore_dir_patterns)]

        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                if not should_ignore_file(file_path, ignore_file_patterns):
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            source = f.read()

                        tree = ast.parse(source)

                        for node in ast.walk(tree):
                            # 处理 import x
                            if isinstance(node, ast.Import):
                                for alias in node.names:
                                    package_name = alias.name.split('.')[0]
                                    if package_name not in STANDARD_LIBRARIES:
                                        all_imports.add(package_name)

                            # 处理 from x import y
                            elif isinstance(node, ast.ImportFrom):
                                if node.module:
                                    package_name = node.module.split('.')[0]
                                    if package_name not in STANDARD_LIBRARIES:
                                        all_imports.add(package_name)
                    except Exception as e:
                        print(f"  解析错误 {file_path}: {e}")

    return all_imports


def write_require_error(source_dir, not_installed_packages):
    """
    将未安装的包写入 requireerror.txt

    Args:
        source_dir: 源目录路径
        not_installed_packages: 未安装的包集合
    """
    if not not_installed_packages:
        return False

    error_file = os.path.join(source_dir, 'requireerror.txt')

    with open(error_file, 'w', encoding='utf-8') as f:
        f.write("# 未安装的第三方库\n")
        f.write(f"# 生成时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("# 以下库在代码中被引用，但 pipreqs 无法获取版本号（可能未安装）:\n\n")

        for package in sorted(not_installed_packages):
            f.write(f"{package}\n")

    print(f"已将未安装的库写入: {error_file}")
    return True


def collect_dependencies(source_dir, output_file, ignore_file_patterns=None, ignore_dir_patterns=None):
    """
    收集 Python 依赖包（使用 pipreqs）

    工作流程：
    1. 提取代码中的所有导入
    2. 运行 pipreqs 生成 requirements.txt
    3. 对比导入和 pipreqs 结果，找出未安装的包
    4. 将未安装的包写入 requireerror.txt

    Args:
        source_dir: 要扫描的源代码目录路径
        output_file: 输出的 requirements.txt 文件路径
        ignore_file_patterns: 忽略文件的正则表达式模式列表
        ignore_dir_patterns: 忽略目录的正则表达式模式列表

    Returns:
        bool: 如果成功返回 True，失败返回 False
    """
    print("=" * 80)
    print("开始收集 Python 依赖包...")
    print("=" * 80)
    print(f"扫描目录: {source_dir}")
    print(f"输出文件: {output_file}")

    # 打印忽略模式
    if ignore_file_patterns:
        print(f"忽略文件模式: {[p.pattern for p in ignore_file_patterns]}")
    if ignore_dir_patterns:
        print(f"忽略目录模式: {[p.pattern for p in ignore_dir_patterns]}")

    print("=" * 80)

    # 创建临时目录
    temp_dir = None
    try:
        # 创建带前缀的临时目录，便于识别和调试
        temp_dir = tempfile.mkdtemp(prefix='pkg_collect_')
        print(f"创建临时目录: {temp_dir}")

        # 复制过滤后的文件到临时目录
        print("正在过滤并复制文件...")
        copy_filtered_files(source_dir, temp_dir, ignore_file_patterns, ignore_dir_patterns)

        # 统计复制的文件数
        python_files = []
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                if file.endswith('.py'):
                    python_files.append(os.path.join(root, file))
        print(f"复制了 {len(python_files)} 个 Python 文件到临时目录")

        # 检查是否找到 Python 文件
        if not python_files:
            print("警告: 没有找到 Python 文件")
            return False

        # 步骤 1: 提取代码中的所有导入
        print("\n步骤 1: 分析代码中的导入...")
        all_imports = extract_all_imports(source_dir, ignore_file_patterns, ignore_dir_patterns)
        print(f"找到 {len(all_imports)} 个第三方库: {', '.join(sorted(all_imports))}")

        # 步骤 2: 运行 pipreqs 生成 requirements.txt
        print("\n步骤 2: 运行 pipreqs 生成 requirements.txt...")
        pipreqs_success, file_generated = run_pipreqs(temp_dir, output_file)

        if not pipreqs_success:
            print("\npipreqs 执行失败")
            return False

        # 步骤 3: 对比结果
        if file_generated and os.path.exists(output_file):
            pipreqs_packages = parse_requirements_file(output_file)
            print(f"pipreqs 检测到 {len(pipreqs_packages)} 个已安装的库")

            # 找出未安装的包
            not_installed = all_imports - set(pipreqs_packages)

            if not_installed:
                print(f"\n找到 {len(not_installed)} 个未安装的库: {', '.join(sorted(not_installed))}")
                write_require_error(source_dir, not_installed)

            print("\n" + "=" * 80)
            print("依赖包收集完成！")
            print("=" * 80)

            # 打印生成的 requirements.txt
            with open(output_file, 'r', encoding='utf-8') as f:
                content = f.read().strip()
            if content:
                print(f"\n生成的 requirements.txt 内容:")
                print(content)
            else:
                print("\nrequirements.txt 为空，所有依赖都在 requireerror.txt 中")
        else:
            print("\n未生成 requirements.txt，所有库可能都未安装")
            write_require_error(source_dir, all_imports)

        return True

    finally:
        # 无论成功与否，都要清理临时目录
        if temp_dir and os.path.exists(temp_dir):
            print(f"\n清理临时目录: {temp_dir}")
            shutil.rmtree(temp_dir)


def analysis(source_dir):
    """
    分析指定目录的 Python 依赖

    Args:
        source_dir: 要分析的源代码目录路径

    Raises:
        AssertionError: 如果源目录不存在
    """
    # 验证源目录存在
    assert os.path.exists(source_dir), FileExistsError(f"源目录不存在: {source_dir}")

    # 设置输出文件路径为源目录下的 requirements.txt
    output_file = os.path.join(source_dir, 'requirements.txt')

    # 构建正则表达式模式（用于过滤）
    ignore_file_patterns, ignore_dir_patterns = build_ignore_patterns()

    # 收集依赖
    success = collect_dependencies(source_dir, output_file, ignore_file_patterns, ignore_dir_patterns)

    # 返回状态码（0 表示成功，1 表示失败）
    sys.exit(0 if success else 1)


# +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+ #

if __name__ == '__main__':
    # 使用 Fire 库创建命令行接口
    # 用法: python pkg_collect.py analysis <source_dir>
    fire.Fire(analysis)  # 注册 analysis 命令
    # p = r"E:\working\working_coding\maya\tools\coding\Playblast"
    # analysis(p)