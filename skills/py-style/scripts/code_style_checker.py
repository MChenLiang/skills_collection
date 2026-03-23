#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
代码风格检查工具

检查 Python 代码是否符合项目的代码风格规范。
"""

import ast
import os
import re
import sys
from pathlib import Path
from typing import List, Dict, Optional, Set, Tuple
from dataclasses import dataclass
from enum import Enum


class Severity(Enum):
    """问题严重程度"""
    ERROR = "ERROR"
    WARNING = "WARNING"
    INFO = "INFO"


@dataclass
class StyleIssue:
    """风格问题"""
    file_path: str
    line: int
    column: int
    severity: Severity
    rule_id: str
    message: str
    suggestion: Optional[str] = None


class CodeStyleChecker:
    """代码风格检查器"""

    def __init__(self, project_root: Optional[str] = None):
        """
        初始化检查器

        Args:
            project_root: 项目根目录
        """
        self.project_root = Path(project_root) if project_root else Path.cwd()
        self.issues: List[StyleIssue] = []
        self._excluded_dirs = {'.git', '__pycache__', '.venv', 'venv', 'node_modules', 'build', 'dist'}
        self._excluded_files = {'__pycache__', '.pyc', '.pyo'}

    def check_file(self, file_path: str) -> List[StyleIssue]:
        """
        检查单个文件

        Args:
            file_path: 文件路径

        Returns:
            发现的风格问题列表
        """
        self.issues = []

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')

            # AST 检查
            self._check_ast(file_path, content, lines)

            # 命名检查
            self._check_naming(file_path, lines)

            # 长度检查
            self._check_line_length(file_path, lines)

            # 空行检查
            self._check_blank_lines(file_path, lines)

            # 导入检查
            self._check_imports(file_path, lines)

            # 文档字符串检查
            self._check_docstrings(file_path, content, lines)

        except Exception as e:
            print(f"Error checking {file_path}: {e}", file=sys.stderr)

        return self.issues

    def check_directory(self, directory: str) -> List[StyleIssue]:
        """
        检查目录下的所有 Python 文件

        Args:
            directory: 目录路径

        Returns:
            发现的风格问题列表
        """
        self.issues = []
        dir_path = Path(directory)

        for file_path in dir_path.rglob('*.py'):
            # 跳过排除的目录和文件
            if self._should_exclude(file_path):
                continue

            self.check_file(str(file_path))

        return self.issues

    def _should_exclude(self, file_path: Path) -> bool:
        """
        检查文件是否应该被排除

        Args:
            file_path: 文件路径

        Returns:
            是否应该排除
        """
        # 检查目录
        for part in file_path.parts:
            if part in self._excluded_dirs:
                return True

        return False

    def _check_ast(self, file_path: str, content: str, lines: List[str]) -> None:
        """
        使用 AST 检查代码

        Args:
            file_path: 文件路径
            content: 文件内容
            lines: 行列表
        """
        try:
            tree = ast.parse(content)

            for node in ast.walk(tree):
                # 检查函数定义
                if isinstance(node, ast.FunctionDef):
                    self._check_function_def(file_path, node, lines)
                # 检查类定义
                elif isinstance(node, ast.ClassDef):
                    self._check_class_def(file_path, node, lines)

        except SyntaxError as e:
            self.issues.append(StyleIssue(
                file_path=file_path,
                line=e.lineno,
                column=e.offset or 0,
                severity=Severity.ERROR,
                rule_id="SYNTAX_ERROR",
                message=f"语法错误: {e.msg}"
            ))

    def _check_function_def(self, file_path: str, node: ast.FunctionDef, lines: List[str]) -> None:
        """
        检查函数定义

        Args:
            file_path: 文件路径
            node: AST 节点
            lines: 行列表
        """
        # 检查函数名是否为小写和下划线
        if not self._is_snake_case(node.name):
            self.issues.append(StyleIssue(
                file_path=file_path,
                line=node.lineno,
                column=node.col_offset,
                severity=Severity.ERROR,
                rule_id="C0103",
                message=f"函数名 '{node.name}' 应该使用 snake_case 命名",
                suggestion=f"重命名为 '{self._to_snake_case(node.name)}'"
            ))

        # 检查是否有文档字符串
        if not (node.body and isinstance(node.body[0], ast.Expr) and
                isinstance(node.body[0].value, (ast.Str, ast.Constant))):
            self.issues.append(StyleIssue(
                file_path=file_path,
                line=node.lineno,
                column=node.col_offset,
                severity=Severity.WARNING,
                rule_id="C0111",
                message=f"函数 '{node.name}' 缺少文档字符串",
                suggestion="添加函数文档字符串"
            ))

        # 检查是否有类型注解
        if not node.returns:
            self.issues.append(StyleIssue(
                file_path=file_path,
                line=node.lineno,
                column=node.col_offset,
                severity=Severity.INFO,
                rule_id="C0104",
                message=f"函数 '{node.name}' 缺少返回类型注解"
            ))

    def _check_class_def(self, file_path: str, node: ast.ClassDef, lines: List[str]) -> None:
        """
        检查类定义

        Args:
            file_path: 文件路径
            node: AST 节点
            lines: 行列表
        """
        # 检查类名是否为大驼峰
        if not self._is_pascal_case(node.name):
            self.issues.append(StyleIssue(
                file_path=file_path,
                line=node.lineno,
                column=node.col_offset,
                severity=Severity.ERROR,
                rule_id="C0103",
                message=f"类名 '{node.name}' 应该使用 PascalCase 命名",
                suggestion=f"重命名为 '{self._to_pascal_case(node.name)}'"
            ))

        # 检查是否有文档字符串
        if not (node.body and isinstance(node.body[0], ast.Expr) and
                isinstance(node.body[0].value, (ast.Str, ast.Constant))):
            self.issues.append(StyleIssue(
                file_path=file_path,
                line=node.lineno,
                column=node.col_offset,
                severity=Severity.WARNING,
                rule_id="C0111",
                message=f"类 '{node.name}' 缺少文档字符串"
            ))

    def _check_naming(self, file_path: str, lines: List[str]) -> None:
        """
        检查命名规范

        Args:
            file_path: 文件路径
            lines: 行列表
        """
        for line_no, line in enumerate(lines, 1):
            # 跳过注释和空行
            stripped = line.strip()
            if not stripped or stripped.startswith('#'):
                continue

            # 检查变量赋值
            # 简单的正则匹配变量赋值
            matches = re.finditer(r'^\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*=', line)
            for match in matches:
                var_name = match.group(1)

                # 跳过特殊变量
                if var_name.startswith('__') or var_name == '_':
                    continue

                # 检查是否为常量（全大写）
                if var_name.isupper():
                    continue

                # 检查是否为 snake_case
                if not self._is_snake_case(var_name):
                    self.issues.append(StyleIssue(
                        file_path=file_path,
                        line=line_no,
                        column=match.start(),
                        severity=Severity.ERROR,
                        rule_id="C0103",
                        message=f"变量名 '{var_name}' 应该使用 snake_case 命名",
                        suggestion=f"重命名为 '{self._to_snake_case(var_name)}'"
                    ))

    def _check_line_length(self, file_path: str, lines: List[str]) -> None:
        """
        检查行长度

        Args:
            file_path: 文件路径
            lines: 行列表
        """
        for line_no, line in enumerate(lines, 1):
            if len(line) > 79:
                self.issues.append(StyleIssue(
                    file_path=file_path,
                    line=line_no,
                    column=79,
                    severity=Severity.WARNING,
                    rule_id="C0301",
                    message=f"行过长 ({len(line)} 字符)，建议不超过 79 字符"
                ))

    def _check_blank_lines(self, file_path: str, lines: List[str]) -> None:
        """
        检查空行使用

        Args:
            file_path: 文件路径
            lines: 行列表
        """
        consecutive_blank = 0

        for line_no, line in enumerate(lines, 1):
            if not line.strip():
                consecutive_blank += 1
                if consecutive_blank > 2:
                    self.issues.append(StyleIssue(
                        file_path=file_path,
                        line=line_no,
                        column=0,
                        severity=Severity.INFO,
                        rule_id="C0303",
                        message="连续空行过多"
                    ))
            else:
                consecutive_blank = 0

    def _check_imports(self, file_path: str, lines: List[str]) -> None:
        """
        检查导入语句

        Args:
            file_path: 文件路径
            lines: 行列表
        """
        import_section = True
        had_standard_lib = False
        had_third_party = False
        had_local = False

        for line_no, line in enumerate(lines, 1):
            stripped = line.strip()

            # 检查是否还有导入语句
            if stripped.startswith('import ') or stripped.startswith('from '):
                # 检查导入顺序
                if self._is_standard_lib_import(stripped):
                    had_standard_lib = True
                    if had_third_party or had_local:
                        self.issues.append(StyleIssue(
                            file_path=file_path,
                            line=line_no,
                            column=0,
                            severity=Severity.WARNING,
                            rule_id="C0411",
                            message="标准库导入应该在第三方库和本地导入之前"
                        ))
                elif self._is_third_party_import(stripped):
                    had_third_party = True
                    if had_local:
                        self.issues.append(StyleIssue(
                            file_path=file_path,
                            line=line_no,
                            column=0,
                            severity=Severity.WARNING,
                            rule_id="C0411",
                            message="第三方库导入应该在本地导入之前"
                        ))
                else:
                    had_local = True
            else:
                # 非导入行
                if import_section and stripped and not stripped.startswith('#'):
                    import_section = False

    def _check_docstrings(self, file_path: str, content: str, lines: List[str]) -> None:
        """
        检查文档字符串

        Args:
            file_path: 文件路径
            content: 文件内容
            lines: 行列表
        """
        # 检查模块文档字符串
        if lines and lines[0].strip().startswith('"""') or lines[0].strip().startswith("'''"):
            # 有模块文档字符串
            pass
        else:
            # 检查是否真的需要模块文档字符串（跳过简单的脚本）
            pass

    def _is_snake_case(self, name: str) -> bool:
        """
        检查是否为 snake_case 命名

        Args:
            name: 名称

        Returns:
            是否为 snake_case
        """
        return bool(re.match(r'^[a-z][a-z0-9_]*$', name))

    def _to_snake_case(self, name: str) -> str:
        """
        转换为 snake_case

        Args:
            name: 名称

        Returns:
            snake_case 名称
        """
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

    def _is_pascal_case(self, name: str) -> bool:
        """
        检查是否为 PascalCase 命名

        Args:
            name: 名称

        Returns:
            是否为 PascalCase
        """
        return bool(re.match(r'^[A-Z][a-zA-Z0-9]*$', name))

    def _to_pascal_case(self, name: str) -> str:
        """
        转换为 PascalCase

        Args:
            name: 名称

        Returns:
            PascalCase 名称
        """
        return ''.join(word.capitalize() for word in name.split('_'))

    def _is_standard_lib_import(self, line: str) -> bool:
        """检查是否为标准库导入"""
        standard_libs = {'os', 'sys', 'json', 're', 'datetime', 'typing', 'logging', 'pathlib'}
        for lib in standard_libs:
            if line.startswith(f'import {lib}') or line.startswith(f'from {lib}'):
                return True
        return False

    def _is_third_party_import(self, line: str) -> bool:
        """检查是否为第三方库导入"""
        third_party = {'numpy', 'pandas', 'requests', 'flask', 'django', 'pytest'}
        for lib in third_party:
            if line.startswith(f'import {lib}') or line.startswith(f'from {lib}'):
                return True
        return False


def print_issues(issues: List[StyleIssue]) -> None:
    """
    打印风格问题

    Args:
        issues: 风格问题列表
    """
    if not issues:
        print("✅ 没有发现风格问题！")
        return

    # 按严重程度排序
    issues.sort(key=lambda x: (x.severity.value, x.file_path, x.line))

    # 统计
    error_count = sum(1 for i in issues if i.severity == Severity.ERROR)
    warning_count = sum(1 for i in issues if i.severity == Severity.WARNING)
    info_count = sum(1 for i in issues if i.severity == Severity.INFO)

    print(f"\n📊 检查结果: {error_count} 错误, {warning_count} 警告, {info_count} 信息\n")

    # 打印问题
    for issue in issues:
        severity_icon = {
            Severity.ERROR: "❌",
            Severity.WARNING: "⚠️",
            Severity.INFO: "ℹ️"
        }.get(issue.severity, "")

        print(f"{severity_icon} {issue.file_path}:{issue.line}:{issue.column}")
        print(f"   {issue.rule_id}: {issue.message}")
        if issue.suggestion:
            print(f"   建议: {issue.suggestion}")
        print()


def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(description='代码风格检查工具')
    parser.add_argument('path', help='文件或目录路径')
    parser.add_argument('--output', '-o', choices=['text', 'json'], default='text',
                        help='输出格式')

    args = parser.parse_args()

    checker = CodeStyleChecker()

    path = Path(args.path)

    if path.is_file():
        issues = checker.check_file(str(path))
    elif path.is_dir():
        issues = checker.check_directory(str(path))
    else:
        print(f"错误: 路径不存在: {args.path}", file=sys.stderr)
        sys.exit(1)

    if args.output == 'json':
        import json
        json_data = [
            {
                'file_path': issue.file_path,
                'line': issue.line,
                'column': issue.column,
                'severity': issue.severity.value,
                'rule_id': issue.rule_id,
                'message': issue.message,
                'suggestion': issue.suggestion
            }
            for issue in issues
        ]
        print(json.dumps(json_data, indent=2))
    else:
        print_issues(issues)

    # 返回退出码
    error_count = sum(1 for i in issues if i.severity == Severity.ERROR)
    sys.exit(min(error_count, 1))


if __name__ == '__main__':
    main()
