#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
批量文件操作工具
支持批量重命名、移动、复制、删除
"""

import os
import shutil
import re
from pathlib import Path
from typing import List, Callable, Optional


class BatchFileOperator:
    """批量文件操作器"""
    
    def __init__(self, base_path: str, pattern: str = "*"):
        """
        初始化操作器
        
        Args:
            base_path: 基础目录
            pattern: 文件匹配模式（如 "*.txt"）
        """
        self.base_path = Path(base_path)
        self.pattern = pattern
        self.files = list(self.base_path.glob(pattern))
    
    def get_files(self) -> List[Path]:
        """
        获取匹配的文件列表
        
        Returns:
            文件路径列表
        """
        return self.files
    
    def rename(
        self,
        old_pattern: str,
        new_pattern: str,
        dry_run: bool = False,
        use_regex: bool = False
    ) -> List[str]:
        """
        批量重命名文件
        
        Args:
            old_pattern: 要替换的旧模式
            new_pattern: 新模式
            dry_run: 是否只显示不实际执行
            use_regex: 是否使用正则表达式
            
        Returns:
            重命名结果列表
        """
        results = []
        
        for file in self.files:
            old_name = file.name
            
            if use_regex:
                new_name = re.sub(old_pattern, new_pattern, old_name)
            else:
                new_name = old_name.replace(old_pattern, new_pattern)
            
            if new_name != old_name:
                new_path = file.parent / new_name
                
                if dry_run:
                    results.append(f"[预览] {old_name} -> {new_name}")
                else:
                    file.rename(new_path)
                    results.append(f"重命名: {old_name} -> {new_name}")
        
        return results
    
    def move_to(
        self,
        target_dir: str,
        create_subdir: bool = False,
        dry_run: bool = False
    ) -> List[str]:
        """
        批量移动文件
        
        Args:
            target_dir: 目标目录
            create_subdir: 是否在目标目录创建子目录
            dry_run: 是否只显示不实际执行
            
        Returns:
            移动结果列表
        """
        results = []
        target_path = Path(target_dir)
        
        if create_subdir:
            target_path = target_path / self.base_path.name
        
        target_path.mkdir(parents=True, exist_ok=True)
        
        for file in self.files:
            if dry_run:
                results.append(f"[预览] 移动: {file.name} -> {target_path / file.name}")
            else:
                shutil.move(str(file), str(target_path / file.name))
                results.append(f"移动: {file.name} -> {target_path / file.name}")
        
        return results
    
    def copy_to(
        self,
        target_dir: str,
        create_subdir: bool = False,
        dry_run: bool = False
    ) -> List[str]:
        """
        批量复制文件
        
        Args:
            target_dir: 目标目录
            create_subdir: 是否在目标目录创建子目录
            dry_run: 是否只显示不实际执行
            
        Returns:
            复制结果列表
        """
        results = []
        target_path = Path(target_dir)
        
        if create_subdir:
            target_path = target_path / self.base_path.name
        
        target_path.mkdir(parents=True, exist_ok=True)
        
        for file in self.files:
            if dry_run:
                results.append(f"[预览] 复制: {file.name} -> {target_path / file.name}")
            else:
                shutil.copy2(str(file), str(target_path / file.name))
                results.append(f"复制: {file.name} -> {target_path / file.name}")
        
        return results
    
    def delete(self, dry_run: bool = False) -> List[str]:
        """
        批量删除文件
        
        Args:
            dry_run: 是否只显示不实际执行
            
        Returns:
            删除结果列表
        """
        results = []
        
        for file in self.files:
            if dry_run:
                results.append(f"[预览] 删除: {file.name}")
            else:
                file.unlink()
                results.append(f"删除: {file.name}")
        
        return results
    
    def apply_date_prefix(self, date_format: str = "%Y%m%d_", dry_run: bool = False) -> List[str]:
        """
        为文件名添加日期前缀
        
        Args:
            date_format: 日期格式
            dry_run: 是否只显示不实际执行
            
        Returns:
            重命名结果列表
        """
        from datetime import datetime
        
        date_prefix = datetime.now().strftime(date_format)
        return self.rename("", date_prefix, dry_run=dry_run)
    
    def apply_suffix(
        self,
        suffix: str,
        position: str = "end",
        dry_run: bool = False
    ) -> List[str]:
        """
        为文件名添加后缀
        
        Args:
            suffix: 后缀内容
            position: 位置 "start" 或 "end" 或 "before_ext"
            dry_run: 是否只显示不实际执行
            
        Returns:
            重命名结果列表
        """
        results = []
        
        for file in self.files:
            old_name = file.stem
            ext = file.suffix
            
            if position == "start":
                new_name = f"{suffix}{old_name}{ext}"
            elif position == "end":
                new_name = f"{old_name}{suffix}{ext}"
            elif position == "before_ext":
                new_name = f"{old_name}{suffix}{ext}"
            else:
                results.append(f"跳过: {file.name} (无效的位置参数)")
                continue
            
            if dry_run:
                results.append(f"[预览] {file.name} -> {new_name}")
            else:
                new_path = file.parent / new_name
                file.rename(new_path)
                results.append(f"重命名: {file.name} -> {new_name}")
        
        return results


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='批量文件操作工具')
    parser.add_argument('path', help='基础目录路径')
    parser.add_argument('--pattern', default='*', help='文件匹配模式')
    
    subparsers = parser.add_subparsers(dest='action', help='操作类型')
    
    # 重命名命令
    rename_parser = subparsers.add_parser('rename', help='批量重命名')
    rename_parser.add_argument('--old', required=True, help='旧模式')
    rename_parser.add_argument('--new', required=True, help='新模式')
    rename_parser.add_argument('--regex', action='store_true', help='使用正则表达式')
    rename_parser.add_argument('--dry-run', action='store_true', help='预览模式')
    
    # 移动命令
    move_parser = subparsers.add_parser('move', help='批量移动')
    move_parser.add_argument('--target', required=True, help='目标目录')
    move_parser.add_argument('--subdir', action='store_true', help='创建子目录')
    move_parser.add_argument('--dry-run', action='store_true', help='预览模式')
    
    # 复制命令
    copy_parser = subparsers.add_parser('copy', help='批量复制')
    copy_parser.add_argument('--target', required=True, help='目标目录')
    copy_parser.add_argument('--subdir', action='store_true', help='创建子目录')
    copy_parser.add_argument('--dry-run', action='store_true', help='预览模式')
    
    # 删除命令
    delete_parser = subparsers.add_parser('delete', help='批量删除')
    delete_parser.add_argument('--dry-run', action='store_true', help='预览模式')
    
    # 添加日期前缀
    date_parser = subparsers.add_parser('date-prefix', help='添加日期前缀')
    date_parser.add_argument('--format', default='%Y%m%d_', help='日期格式')
    date_parser.add_argument('--dry-run', action='store_true', help='预览模式')
    
    args = parser.parse_args()
    
    if not args.action:
        parser.print_help()
        return
    
    operator = BatchFileOperator(args.path, args.pattern)
    
    if args.action == 'rename':
        results = operator.rename(
            args.old,
            args.new,
            dry_run=args.dry_run,
            use_regex=args.regex
        )
    elif args.action == 'move':
        results = operator.move_to(
            args.target,
            create_subdir=args.subdir,
            dry_run=args.dry_run
        )
    elif args.action == 'copy':
        results = operator.copy_to(
            args.target,
            create_subdir=args.subdir,
            dry_run=args.dry_run
        )
    elif args.action == 'delete':
        results = operator.delete(dry_run=args.dry_run)
    elif args.action == 'date-prefix':
        results = operator.apply_date_prefix(
            date_format=args.format,
            dry_run=args.dry_run
        )
    else:
        print(f"未知操作: {args.action}")
        return
    
    for result in results:
        print(result)


if __name__ == "__main__":
    main()
