#!/usr/bin/env python
# -*- coding: UTF-8 -*-


from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import os
import ast
import shutil
import re
import fnmatch
import sys
import fire
from collections import defaultdict
from typing import Dict, Set, List, Tuple, Optional

# 检查Python版本
PY_VERSION = sys.version_info

# 配置常量
PRESERVED_NAMES = {
    'main', 'register', 'unregister', 'ui', 'create_ui',
    'initializePlugin', 'uninitializePlugin', 'encryption'
}


def is_event_function(func_name: str) -> bool:
    """检查函数名是否为事件处理函数（以 Event 结尾）"""
    return func_name.endswith('Event')


def safe_unparse(node) -> str:
    """
    安全地将AST节点转换为字符串，兼容不同Python版本

    参数:
        node: AST节点

    返回:
        节点的字符串表示
    """
    if PY_VERSION >= (3, 9):
        try:
            return ast.unparse(node).split('(')[0]
        except:
            return _extract_decorator_name_fallback(node)
    else:
        return _extract_decorator_name_fallback(node)


def _extract_decorator_name_fallback(node) -> str:
    """
    备用方案：手动提取装饰器名称（兼容Python 3.8及以下版本）

    参数:
        node: 装饰器节点

    返回:
        装饰器名称字符串
    """
    if isinstance(node, ast.Name):
        return node.id
    elif isinstance(node, ast.Attribute):
        return node.attr
    elif isinstance(node, ast.Call):
        if isinstance(node.func, ast.Name):
            return node.func.id
        elif isinstance(node.func, ast.Attribute):
            return node.func.attr
    return ""


def get_decorator_name(node) -> str:
    """
    获取装饰器名称

    参数:
        node: 装饰器节点

    返回:
        装饰器名称
    """
    if hasattr(ast, 'unparse') and PY_VERSION >= (3, 9):
        try:
            return ast.unparse(node).split('(')[0]
        except:
            return _extract_decorator_name_fallback(node)
    else:
        return _extract_decorator_name_fallback(node)


class ExcludePatterns:
    """
    排除模式配置
    """

    # 默认排除的目录
    DEFAULT_EXCLUDE_DIRS = {
        '__pycache__', '.git', '.svn', '.hg',
        'venv', 'env', '.env', 'virtualenv',
        'build', 'dist', '*.egg-info',
        '.idea', '.vscode', '.vs',
        'tests', 'test', 'testing',
        'docs', 'doc', 'examples', 'data',
        'migrations', 'migration', 'site-packages', 'third_party', 'third-party', 'UI',
        # Rez/Build 特定目录
        'other', 'file', 'tmp', 'config_zip',
        'fix', 'icons_del', 'Texture', 'delete', 'del'
    }

    # 默认排除的文件模式
    DEFAULT_EXCLUDE_FILES = {
        'setup.py', 'conf.py', 'conftest.py',
        'test_*.py', '*_test.py', 'test*.py', 'package.py',
        '*_backup.py', 'verify.py', 'resources.py', 'script_tool.py',
        'rez_*.py', '*build.py', 'auto_pep8.py', 'builder.py',
        'pkg_collect.bat', 'requirements.txt', 'additional_assemble_script.py',
        'ctrl.py', 'clearn.py',
        '__init__.py', '__main__.py',
        '*.pyc', '*.pyo', '*.pyd',
        '*.so', '*.dll', '*.dylib', 'Qt.py'
    }

    # 保留的文件（不分析但保留）
    PRESERVED_FILES = {
        '__init__.py', 'script_tool.py',
        'additional_assemble_script.py', 'resources.py'
    }

    # 保留的目录（不分析其中的文件）
    PRESERVED_DIRS = {
        'exe', 'site-packages', 'third-party', 'plug-ins', 'icons'
    }

    @classmethod
    def matches_pattern(cls, path: str, pattern: str) -> bool:
        """检查路径是否匹配排除模式"""
        # 目录匹配
        if pattern.endswith('/') or pattern.endswith('\\'):
            dir_pattern = pattern.rstrip('/\\')
            return any(part == dir_pattern for part in path.split(os.sep))

        # 文件匹配（支持通配符）
        return fnmatch.fnmatch(os.path.basename(path), pattern)


class FileExcluder:
    """文件排除管理器"""

    def __init__(self,
                 exclude_dirs: Optional[Set[str]] = None,
                 exclude_files: Optional[Set[str]] = None,
                 exclude_patterns: Optional[List[str]] = None):
        """
        初始化排除管理器

        参数:
            exclude_dirs: 要排除的目录名集合
            exclude_files: 要排除的文件名模式集合
            exclude_patterns: 自定义排除模式列表（完整路径匹配）
        """
        self.exclude_dirs = set(ExcludePatterns.DEFAULT_EXCLUDE_DIRS)
        self.exclude_files = set(ExcludePatterns.DEFAULT_EXCLUDE_FILES)
        self.preserved_files = set(ExcludePatterns.PRESERVED_FILES)
        self.preserved_dirs = set(ExcludePatterns.PRESERVED_DIRS)
        self.custom_patterns = []

        if exclude_dirs:
            self.exclude_dirs.update(exclude_dirs)

        if exclude_files:
            self.exclude_files.update(exclude_files)

        if exclude_patterns:
            self.custom_patterns.extend(exclude_patterns)

    def should_exclude(self, file_path: str, root_dir: str) -> bool:
        """
        判断文件是否应该被排除

        参数:
            file_path: 文件的完整路径
            root_dir: 根目录路径

        返回:
            True表示应该排除，False表示应该包含
        """
        rel_path = os.path.relpath(file_path, root_dir)
        filename = os.path.basename(file_path)

        # 检查是否在保留的文件列表中
        if filename in self.preserved_files:
            return True  # 保留但不分析

        # 检查自定义模式
        for pattern in self.custom_patterns:
            if fnmatch.fnmatch(rel_path, pattern):
                return True

        # 检查目录排除
        path_parts = rel_path.split(os.sep)
        for part in path_parts[:-1]:  # 排除目录部分
            if part in self.exclude_dirs or part in self.preserved_dirs:
                return True

        # 检查文件排除
        for file_pattern in self.exclude_files:
            if ExcludePatterns.matches_pattern(filename, file_pattern):
                return True

        return False

    def filter_files(self, files: List[str], root_dir: str) -> List[str]:
        """过滤文件列表，返回应该包含的文件"""
        return [f for f in files if not self.should_exclude(f, root_dir)]

    def add_exclude_dir(self, dir_name: str):
        """添加要排除的目录"""
        self.exclude_dirs.add(dir_name)

    def add_exclude_file(self, file_pattern: str):
        """添加要排除的文件模式"""
        self.exclude_files.add(file_pattern)

    def add_custom_pattern(self, pattern: str):
        """添加自定义排除模式"""
        self.custom_patterns.append(pattern)

    def get_exclude_summary(self) -> Dict:
        """获取排除规则摘要"""
        return {
            'exclude_dirs'   : sorted(self.exclude_dirs),
            'exclude_files'  : sorted(self.exclude_files),
            'preserved_files': sorted(self.preserved_files),
            'preserved_dirs' : sorted(self.preserved_dirs),
            'custom_patterns': self.custom_patterns
        }


class FunctionCleaner:
    """函数清理执行器"""

    def __init__(self, package_path: str, backup: bool = True):
        self.package_path = package_path
        self.backup = backup
        self.backup_dir = None

    def setup_backup(self) -> Optional[str]:
        """设置备份目录"""
        if self.backup:
            self.backup_dir = os.path.join(self.package_path, ".backup_cleaner")
            if not os.path.exists(self.backup_dir):
                os.makedirs(self.backup_dir)
        return self.backup_dir

    def backup_file(self, file_path: str) -> Optional[str]:
        """备份单个文件"""
        if not self.backup_dir:
            return None

        backup_path = os.path.join(self.backup_dir, os.path.basename(file_path))
        # 避免重复备份
        if not os.path.exists(backup_path):
            shutil.copy2(file_path, backup_path)
            return backup_path
        return None

    def find_function_block(self, lines: List[str], start_line: int) -> int:
        """查找函数代码块的结束行"""
        if start_line >= len(lines):
            return start_line + 1

        # 获取函数的缩进级别
        first_line = lines[start_line]
        indent = len(first_line) - len(first_line.lstrip())

        for i in range(start_line + 1, len(lines)):
            line = lines[i]
            # 跳过空行和注释
            if not line.strip() or line.strip().startswith('#'):
                continue

            current_indent = len(line) - len(line.lstrip())
            # 当缩进级别小于等于函数缩进时，表示函数结束
            if current_indent <= indent and line.strip():
                return i

        return len(lines)

    def remove_functions_from_file(self, file_path: str, nodes: List[ast.FunctionDef]) -> bool:
        """从文件中移除指定的函数"""
        try:
            # 读取文件
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            # 备份
            backup_path = self.backup_file(file_path)
            if backup_path:
                print(f"  已备份: {os.path.basename(backup_path)}")

            # 按行号倒序排序，从后往前删除
            nodes_sorted = sorted(nodes, key=lambda n: n.lineno, reverse=True)
            removed_count = 0

            for node in nodes_sorted:
                start_idx = node.lineno - 1
                end_idx = self.find_function_block(lines, start_idx)

                # 记录被删除的函数信息
                print(f"  删除函数 {node.name} (行 {node.lineno}-{end_idx})")

                # 执行删除
                del lines[start_idx:end_idx]
                removed_count += 1

            # 写回文件
            with open(file_path, 'w', encoding='utf-8') as f:
                f.writelines(lines)

            return True

        except Exception as e:
            print(f"  清理失败 {file_path}: {e}")
            return False

    def clean_files(self, unused_funcs: Dict[str, List]) -> Dict[str, int]:
        """清理多个文件中的未使用函数"""
        results = {}

        for file_path, nodes in unused_funcs.items():
            print(f"\n处理文件: {os.path.relpath(file_path, self.package_path)}")
            success = self.remove_functions_from_file(file_path, nodes)
            results[file_path] = len(nodes) if success else 0

        return results


class UsageCollector(ast.NodeVisitor):
    """AST节点访问器，收集所有名称使用情况"""

    def __init__(self):
        self.used_names = set()
        self.qt_connections = set()
        self.class_hierarchy = {}

    def visit_Call(self, node: ast.Call):
        """访问函数调用"""
        # 处理普通调用
        if isinstance(node.func, ast.Name):
            self.used_names.add(node.func.id)
        elif isinstance(node.func, ast.Attribute):
            self.used_names.add(node.func.attr)

            # 检测Qt连接模式: object.signal.connect(slot)
            if node.func.attr == 'connect' and node.args:
                self._check_qt_connection(node)

        self.generic_visit(node)

    def _check_qt_connection(self, node: ast.Call):
        """检查是否为Qt信号连接"""
        if node.args and isinstance(node.args[0], ast.Name):
            # 直接函数名: button.clicked.connect(self.on_click)
            self.used_names.add(node.args[0].id)
            self.qt_connections.add(node.args[0].id)
        elif node.args and isinstance(node.args[0], ast.Attribute):
            # 属性方法: button.clicked.connect(self.on_click)
            self.used_names.add(node.args[0].attr)
            self.qt_connections.add(node.args[0].attr)

    def visit_Attribute(self, node: ast.Attribute):
        """访问属性访问"""
        # 处理方法调用中的属性
        self.used_names.add(node.attr)
        self.generic_visit(node)

    def visit_Import(self, node: ast.Import):
        """访问导入语句"""
        for alias in node.names:
            name = alias.name.split('.')[0]
            self.used_names.add(name)
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom):
        """访问from导入语句"""
        for alias in node.names:
            self.used_names.add(alias.name)
        self.generic_visit(node)

    def visit_ClassDef(self, node: ast.ClassDef):
        """访问类定义"""
        # 记录类继承关系
        bases = []
        for base in node.bases:
            if isinstance(base, ast.Name):
                bases.append(base.id)
            elif isinstance(base, ast.Attribute):
                bases.append(base.attr)

        self.class_hierarchy[node.name] = bases
        self.generic_visit(node)


class QtPatterns:
    """Qt相关模式识别"""

    # Qt信号命名模式
    SIGNAL_PATTERNS = [
        r'^on_\w+_\w+$',  # on_object_signal 格式
        r'^on_\w+$',  # on_signal 格式
        r'^slot_\w+$',  # slot_name 格式
        r'^_\w+_slot$',  # _name_slot 格式
        r'^triggered_\w+$',  # triggered_action 格式
        r'^clicked_\w+$',  # clicked_button 格式
        r'^activated_\w+$',  # activated_menu 格式
    ]

    # Qt装饰器模式
    QT_DECORATORS = {
        '@Slot', '@pyqtSlot', '@QtCore.Slot',
        '@Signal', '@pyqtSignal', '@QtCore.Signal',
        '@Property', '@pyqtProperty', '@QtCore.Property'
    }

    @classmethod
    def is_qt_signal_handler(cls, func_name: str) -> bool:
        """判断是否为Qt信号处理函数"""
        for pattern in cls.SIGNAL_PATTERNS:
            if re.match(pattern, func_name, re.IGNORECASE):
                return True
        return False

    @classmethod
    def has_qt_decorator(cls, node: ast.FunctionDef) -> bool:
        """检查函数是否有Qt装饰器"""
        for decorator in node.decorator_list:
            decorator_str = get_decorator_name(decorator)
            if decorator_str in cls.QT_DECORATORS:
                return True
        return False


class FunctionUsageAnalyzer:
    """函数使用情况分析器"""

    def __init__(self, package_path: str, excluder: Optional[FileExcluder] = None):
        """
        初始化分析器

        参数:
            package_path: 包路径
            excluder: 文件排除管理器
        """
        self.package_path = package_path
        self.excluder = excluder or FileExcluder()
        self.all_functions: Dict[str, Dict] = {}
        self.used_names: Set[str] = set()
        self.qt_connections: Set[str] = set()
        self.class_methods: Dict[str, Set[str]] = defaultdict(set)
        self.py_files: List[str] = []
        self.excluded_files: List[str] = []

    def find_python_files(self) -> Tuple[List[str], List[str]]:
        """
        查找包中的所有Python文件

        返回:
            (包含的文件列表, 排除的文件列表)
        """
        included = []
        excluded = []

        for root, dirs, files in os.walk(self.package_path):
            # 修改dirs以跳过排除的目录（优化性能）
            dirs[:] = [d for d in dirs if d not in self.excluder.exclude_dirs and d not in self.excluder.preserved_dirs]

            for f in files:
                if f.endswith('.py'):
                    full_path = os.path.join(root, f)

                    if self.excluder.should_exclude(full_path, self.package_path):
                        excluded.append(full_path)
                    else:
                        included.append(full_path)

        self.py_files = included
        self.excluded_files = excluded
        return included, excluded

    def analyze_file(self, file_path: str) -> Tuple[Dict, Set, Set]:
        """分析单个文件"""
        file_functions = {}

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                source = f.read()

            tree = ast.parse(source)
            collector = UsageCollector()
            collector.visit(tree)

            # 收集函数定义
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    func_info = self._extract_function_info(node, file_path)
                    file_functions[node.name] = func_info

                    # 如果是类方法，记录到类方法集合
                    if func_info['class_name']:
                        self.class_methods[func_info['class_name']].add(node.name)

            return file_functions, collector.used_names, collector.qt_connections

        except Exception as e:
            print(f"解析错误 {file_path}: {e}")
            return {}, set(), set()

    def _extract_function_info(self, node: ast.FunctionDef, file_path: str) -> Dict:
        """提取函数信息"""
        # 查找所属的类
        class_name = None
        for parent in ast.walk(node):
            if isinstance(parent, ast.ClassDef):
                for child in parent.body:
                    if child is node:
                        class_name = parent.name
                        break

        # 安全地获取装饰器名称
        decorators = []
        for decorator in node.decorator_list:
            decorator_name = get_decorator_name(decorator)
            if decorator_name:
                decorators.append(decorator_name)

        return {
            'file'            : file_path,
            'node'            : node,
            'start_line'      : node.lineno,
            'end_line'        : self._find_node_end(node),
            'class_name'      : class_name,
            'decorators'      : decorators,
            'has_qt_decorator': QtPatterns.has_qt_decorator(node)
        }

    def _find_node_end(self, node) -> int:
        """查找节点的结束行号"""
        if hasattr(node, 'end_lineno') and node.end_lineno:
            return node.end_lineno

        max_line = node.lineno
        for child in ast.walk(node):
            if hasattr(child, 'lineno') and child.lineno > max_line:
                max_line = child.lineno
        return max_line

    def analyze_all(self) -> Tuple[Dict[str, List], Set[str]]:
        """分析所有文件"""
        included, excluded = self.find_python_files()

        print(f"找到 {len(included)} 个Python文件需要分析")
        if excluded:
            print(f"排除 {len(excluded)} 个文件")

        all_used_names = set()
        all_qt_connections = set()

        for file_path in included:
            file_funcs, used_names, qt_conns = self.analyze_file(file_path)
            self.all_functions.update(file_funcs)
            all_used_names.update(used_names)
            all_qt_connections.update(qt_conns)

        self.used_names = all_used_names
        self.qt_connections = all_qt_connections

        return self.all_functions, self.used_names

    def find_unused_functions(self) -> Dict[str, List[ast.FunctionDef]]:
        """查找未使用的函数，考虑Qt特性"""
        unused_by_file = defaultdict(list)

        for name, info in self.all_functions.items():
            if self._is_function_used(name, info):
                continue

            # 双重检查：可能在类方法中被使用
            if self._is_method_used_indirectly(name, info):
                continue

            unused_by_file[info['file']].append(info['node'])

        return dict(unused_by_file)

    def _is_function_used(self, func_name: str, info: Dict) -> bool:
        """判断函数是否被使用（考虑Qt特性）"""
        # 直接使用
        if func_name in self.used_names:
            return True

        # Qt信号连接
        if func_name in self.qt_connections:
            return True

        # Qt信号处理函数模式
        if QtPatterns.is_qt_signal_handler(func_name):
            return True

        # 有Qt装饰器
        if info['has_qt_decorator']:
            return True

        # 保留名称
        if func_name in PRESERVED_NAMES:
            return True

        # 事件函数（以 Event 结尾）
        if is_event_function(func_name):
            return True

        # 特殊方法
        if func_name.startswith('__') and func_name.endswith('__'):
            return True

        return False

    def _is_method_used_indirectly(self, method_name: str, info: Dict) -> bool:
        """检查方法是否被间接使用"""
        if not info['class_name']:
            return False

        # 检查是否是重写的Qt方法
        qt_methods = {'show', 'hide', 'close', 'paintEvent', 'mousePressEvent',
                      'keyPressEvent', 'resizeEvent', 'contextMenuEvent'}

        if method_name in qt_methods:
            return True

        return False

    def get_unused_summary(self, unused_funcs: Dict[str, List]) -> Dict:
        """生成未使用函数的统计摘要"""
        summary = {
            'total_count'       : sum(len(v) for v in unused_funcs.values()),
            'files_count'       : len(unused_funcs),
            'by_file'           : {},
            'qt_signal_handlers': [],
            'excluded_files'    : self.excluded_files
        }

        for file_path, nodes in unused_funcs.items():
            rel_path = os.path.relpath(file_path, self.package_path)
            file_funcs = []

            for node in nodes:
                func_info = {
                    'name'        : node.name,
                    'line'        : node.lineno,
                    'is_qt_signal': QtPatterns.is_qt_signal_handler(node.name)
                }
                file_funcs.append(func_info)

                if func_info['is_qt_signal']:
                    summary['qt_signal_handlers'].append({
                        'file': rel_path,
                        'name': node.name,
                        'line': node.lineno
                    })

            summary['by_file'][rel_path] = file_funcs

        return summary


def find_unused_functions(package_path: str,
                          exclude_dirs: Optional[Set[str]] = None,
                          exclude_files: Optional[Set[str]] = None,
                          exclude_patterns: Optional[List[str]] = None) -> Tuple[Dict[str, List], Dict]:
    """
    查找未使用的函数，支持文件排除

    参数:
        package_path: 包路径
        exclude_dirs: 要排除的目录名集合
        exclude_files: 要排除的文件名模式集合
        exclude_patterns: 自定义排除模式列表

    返回:
        (未使用函数字典, 统计摘要)
    """
    excluder = FileExcluder(exclude_dirs, exclude_files, exclude_patterns)

    print(f"正在扫描: {package_path}")
    print("排除规则:")
    summary = excluder.get_exclude_summary()
    if summary['exclude_dirs']:
        print(f"  排除目录: {', '.join(summary['exclude_dirs'][:10])}")
        if len(summary['exclude_dirs']) > 10:
            print(f"    ... 等 {len(summary['exclude_dirs'])} 个")
    if summary['exclude_files']:
        print(f"  排除文件: {', '.join(summary['exclude_files'][:10])}")
    if summary['preserved_dirs']:
        print(f"  保留目录: {', '.join(summary['preserved_dirs'])}")
    if summary['custom_patterns']:
        print(f"  自定义模式: {', '.join(summary['custom_patterns'])}")

    analyzer = FunctionUsageAnalyzer(package_path, excluder)
    all_funcs, used_names = analyzer.analyze_all()

    print(f"找到 {len(all_funcs)} 个函数定义")
    print(f"找到 {len(used_names)} 个被直接使用的名称")
    print(f"找到 {len(analyzer.qt_connections)} 个Qt信号连接")

    # 识别Qt信号处理函数
    qt_handlers = []
    for name, info in all_funcs.items():
        if QtPatterns.is_qt_signal_handler(name) or info['has_qt_decorator']:
            qt_handlers.append(name)

    print(f"识别到 {len(qt_handlers)} 个Qt信号处理函数")

    unused_funcs = analyzer.find_unused_functions()
    summary = analyzer.get_unused_summary(unused_funcs)

    # 显示Qt信号处理函数的警告
    if summary['qt_signal_handlers']:
        print("\n⚠️  注意: 以下函数看起来像Qt信号处理函数，但未被检测到使用:")
        for item in summary['qt_signal_handlers'][:10]:  # 只显示前10个
            print(f"  - {item['file']}: {item['name']} (行 {item['line']})")
        if len(summary['qt_signal_handlers']) > 10:
            print(f"    ... 等 {len(summary['qt_signal_handlers'])} 个")
        print("  如果这些函数是通过UI文件自动连接的，请确认后再决定是否删除。\n")

    return unused_funcs, summary


def clean_unused_functions(package_path: str,
                           dry_run: bool = True,
                           backup: bool = True,
                           safe_mode: bool = True,
                           exclude_dirs: Optional[Set[str]] = None,
                           exclude_files: Optional[Set[str]] = None,
                           exclude_patterns: Optional[List[str]] = None) -> Dict:
    """
    清理未使用的函数，支持文件排除

    参数:
        package_path: 包路径
        dry_run: 预览模式
        backup: 是否备份
        safe_mode: 安全模式（不删除看起来像Qt信号处理函数的函数）
        exclude_dirs: 要排除的目录名集合
        exclude_files: 要排除的文件名模式集合
        exclude_patterns: 自定义排除模式列表

    返回:
        操作结果统计
    """
    # 查找未使用的函数
    unused_funcs, summary = find_unused_functions(
        package_path,
        exclude_dirs,
        exclude_files,
        exclude_patterns
    )

    if summary['total_count'] == 0:
        print("\n未发现未使用的函数。")
        return {'status': 'no_unused_functions'}

    # 安全模式：过滤掉Qt信号处理函数
    if safe_mode and summary['qt_signal_handlers']:
        filtered_unused = defaultdict(list)
        filtered_count = 0

        for file_path, nodes in unused_funcs.items():
            for node in nodes:
                if not QtPatterns.is_qt_signal_handler(node.name):
                    filtered_unused[file_path].append(node)
                else:
                    filtered_count += 1

        if filtered_count > 0:
            print(f"\n安全模式: 保留了 {filtered_count} 个Qt信号处理函数")
            unused_funcs = dict(filtered_unused)
            # 重新计算摘要
            analyzer = FunctionUsageAnalyzer(package_path)
            summary = analyzer.get_unused_summary(unused_funcs)

    if summary['total_count'] == 0:
        print("\n安全模式下无函数可删除。")
        return {'status': 'no_unused_functions_safe_mode'}

    # 显示摘要
    print(f"\n将处理 {summary['total_count']} 个未使用的函数，分布在 {summary['files_count']} 个文件中:")

    for rel_path, funcs in list(summary['by_file'].items())[:10]:  # 只显示前10个文件
        print(f"\n  {rel_path}:")
        for func in funcs[:5]:  # 每个文件只显示前5个函数
            qt_mark = " [Qt信号]" if func['is_qt_signal'] else ""
            print(f"    - {func['name']} (行 {func['line']}){qt_mark}")
        if len(funcs) > 5:
            print(f"    ... 等 {len(funcs)} 个函数")

    if len(summary['by_file']) > 10:
        print(f"\n    ... 等 {len(summary['by_file']) - 10} 个文件")

    if dry_run:
        print(f"\n[预览模式] 以上 {summary['total_count']} 个函数将被移除。")
        print("设置 dry_run=False 以执行实际操作。")
        return {
            'status' : 'preview',
            'dry_run': True,
            'summary': summary
        }

    # 执行清理
    print(f"\n开始清理 {summary['total_count']} 个未使用的函数...")

    cleaner = FunctionCleaner(package_path, backup)
    cleaner.setup_backup()

    results = cleaner.clean_files(unused_funcs)
    cleaned_count = sum(results.values())

    print(f"\n清理完成！成功移除 {cleaned_count} 个函数。")

    if backup:
        print(f"备份文件保存在: {cleaner.backup_dir}")

    return {
        'status'               : 'success',
        'cleaned_count'        : cleaned_count,
        'files_processed'      : len(results),
        'backup_dir'           : cleaner.backup_dir,
        'qt_handlers_preserved': len(summary['qt_signal_handlers']) if safe_mode else 0,
        'excluded_files'       : summary['excluded_files']
    }


# 便捷函数
def preview_unused_functions(package_path: str,
                             safe_mode: bool = True,
                             exclude_dirs: Optional[Set[str]] = None,
                             exclude_files: Optional[Set[str]] = None,
                             exclude_patterns: Optional[List[str]] = None) -> Dict:
    """预览未使用的函数"""
    return clean_unused_functions(
        package_path,
        dry_run=True,
        backup=False,
        safe_mode=safe_mode,
        exclude_dirs=exclude_dirs,
        exclude_files=exclude_files,
        exclude_patterns=exclude_patterns
    )


def remove_unused_functions(package_path: str,
                            backup: bool = True,
                            safe_mode: bool = True,
                            exclude_dirs: Optional[Set[str]] = None,
                            exclude_files: Optional[Set[str]] = None,
                            exclude_patterns: Optional[List[str]] = None) -> Dict:
    """移除未使用的函数"""
    return clean_unused_functions(
        package_path,
        dry_run=False,
        backup=backup,
        safe_mode=safe_mode,
        exclude_dirs=exclude_dirs,
        exclude_files=exclude_files,
        exclude_patterns=exclude_patterns
    )


def quick_clean(package_path: str, ) -> Dict:
    """快速清理"""
    return clean_unused_functions(
        package_path,
        dry_run=False,
        backup=True,
        safe_mode=True,
    )


def quick_preview(package_path: str, ) -> Dict:
    """快速预览"""
    return preview_unused_functions(
        package_path,
        safe_mode=True,
    )


# 使用示例
if __name__ == "__main__":
    fire.Fire({
        'preview': preview_unused_functions,
        'clean'  : remove_unused_functions,
        'quick_preview': quick_preview,
        'quick_clean'  : quick_clean,
    })
