#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Git 操作助手
提供常用的 Git 操作封装
"""

import os
import subprocess
from pathlib import Path
from typing import Optional, List, Dict


class GitHelper:
    """Git 操作助手"""
    
    def __init__(self, repo_path: str):
        """
        初始化 Git 助手
        
        Args:
            repo_path: Git 仓库路径
        """
        self.repo_path = Path(repo_path).absolute()
    
    def _run_command(
        self,
        command: List[str],
        capture_output: bool = True
    ) -> Dict[str, any]:
        """
        运行 Git 命令
        
        Args:
            command: 命令列表
            capture_output: 是否捕获输出
            
        Returns:
            包含 returncode, stdout, stderr 的字典
        """
        try:
            result = subprocess.run(
                ['git'] + command,
                cwd=self.repo_path,
                capture_output=capture_output,
                text=True,
                encoding='utf-8'
            )
            
            return {
                'returncode': result.returncode,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'success': result.returncode == 0
            }
        except Exception as e:
            return {
                'returncode': -1,
                'stdout': '',
                'stderr': str(e),
                'success': False
            }
    
    def status(self) -> Dict[str, any]:
        """
        获取仓库状态
        
        Returns:
            状态信息
        """
        return self._run_command(['status', '--short'])
    
    def pull(self, remote: str = 'origin', branch: str = 'master') -> Dict[str, any]:
        """
        拉取最新代码
        
        Args:
            remote: 远程仓库名
            branch: 分支名
            
        Returns:
            执行结果
        """
        print(f"正在拉取代码: {remote}/{branch}")
        result = self._run_command(['pull', remote, branch])
        
        if result['success']:
            print("代码拉取成功")
        else:
            print(f"代码拉取失败: {result['stderr']}")
        
        return result
    
    def push(
        self,
        remote: str = 'origin',
        branch: str = 'master',
        force: bool = False
    ) -> Dict[str, any]:
        """
        推送代码
        
        Args:
            remote: 远程仓库名
            branch: 分支名
            force: 是否强制推送
            
        Returns:
            执行结果
        """
        cmd = ['push']
        if force:
            cmd.append('-f')
        cmd.extend([remote, branch])
        
        print(f"正在推送代码: {remote}/{branch}")
        result = self._run_command(cmd)
        
        if result['success']:
            print("代码推送成功")
        else:
            print(f"代码推送失败: {result['stderr']}")
        
        return result
    
    def add(self, files: str = '.') -> Dict[str, any]:
        """
        添加文件到暂存区
        
        Args:
            files: 文件路径（默认为所有文件）
            
        Returns:
            执行结果
        """
        return self._run_command(['add', files])
    
    def commit(
        self,
        message: str,
        amend: bool = False
    ) -> Dict[str, any]:
        """
        提交更改
        
        Args:
            message: 提交信息
            amend: 是否修改最后一次提交
            
        Returns:
            执行结果
        """
        cmd = ['commit', '-m', message]
        if amend:
            cmd.append('--amend')
        
        return self._run_command(cmd)
    
    def create_branch(
        self,
        branch_name: str,
        checkout: bool = True
    ) -> Dict[str, any]:
        """
        创建新分支
        
        Args:
            branch_name: 分支名
            checkout: 是否切换到新分支
            
        Returns:
            执行结果
        """
        cmd = ['branch', branch_name]
        if checkout:
            cmd = ['checkout', '-b', branch_name]
        
        return self._run_command(cmd)
    
    def checkout(self, branch: str) -> Dict[str, any]:
        """
        切换分支
        
        Args:
            branch: 分支名
            
        Returns:
            执行结果
        """
        return self._run_command(['checkout', branch])
    
    def get_branches(self) -> Dict[str, any]:
        """
        获取所有分支
        
        Returns:
            分支列表
        """
        result = self._run_command(['branch', '-a'])
        return result
    
    def get_current_branch(self) -> Optional[str]:
        """
        获取当前分支
        
        Returns:
            当前分支名
        """
        result = self._run_command(['rev-parse', '--abbrev-ref', 'HEAD'])
        if result['success']:
            return result['stdout'].strip()
        return None
    
    def clone(
        self,
        url: str,
        destination: Optional[str] = None
    ) -> Dict[str, any]:
        """
        克隆仓库
        
        Args:
            url: 仓库 URL
            destination: 目标路径
            
        Returns:
            执行结果
        """
        cmd = ['clone', url]
        if destination:
            cmd.append(destination)
        
        return self._run_command(cmd)
    
    def log(
        self,
        max_count: int = 10,
        format_str: str = '%h - %s (%an, %ar)'
    ) -> Dict[str, any]:
        """
        获取提交日志
        
        Args:
            max_count: 最大显示数量
            format_str: 日志格式
            
        Returns:
            提交日志
        """
        return self._run_command([
            'log',
            f'--max-count={max_count}',
            f'--format={format_str}'
        ])
    
    def stash(self, message: str = '') -> Dict[str, any]:
        """
        暂存当前更改
        
        Args:
            message: 暂存信息
            
        Returns:
            执行结果
        """
        if message:
            return self._run_command(['stash', 'push', '-m', message])
        return self._run_command(['stash'])
    
    def stash_pop(self) -> Dict[str, any]:
        """
        恢复暂存的更改
        
        Returns:
            执行结果
        """
        return self._run_command(['stash', 'pop'])
    
    def reset(self, mode: str = 'hard', commit: str = 'HEAD') -> Dict[str, any]:
        """
        重置仓库
        
        Args:
            mode: 模式 (soft, mixed, hard)
            commit: 目标提交
            
        Returns:
            执行结果
        """
        return self._run_command(['reset', f'--{mode}', commit])


def main():
    """主函数"""
    import argparse
    import json
    
    parser = argparse.ArgumentParser(description='Git 操作助手')
    parser.add_argument('--path', default='.', help='Git 仓库路径')
    parser.add_argument('--remote', default='origin', help='远程仓库名')
    parser.add_argument('--branch', help='分支名')
    parser.add_argument('--json', action='store_true', help='JSON 格式输出')
    
    subparsers = parser.add_subparsers(dest='action', help='操作类型')
    
    subparsers.add_parser('status', help='查看状态')
    subparsers.add_parser('pull', help='拉取代码')
    subparsers.add_parser('push', help='推送代码')
    
    branch_parser = subparsers.add_parser('branches', help='查看分支')
    branch_parser.add_argument('--all', action='store_true', help='显示所有分支')
    
    log_parser = subparsers.add_parser('log', help='查看日志')
    log_parser.add_argument('--count', type=int, default=10, help='显示数量')
    
    args = parser.parse_args()
    
    if not args.action:
        parser.print_help()
        return
    
    helper = GitHelper(args.path)
    
    if args.action == 'status':
        result = helper.status()
    elif args.action == 'pull':
        branch = args.branch or helper.get_current_branch()
        result = helper.pull(remote=args.remote, branch=branch)
    elif args.action == 'push':
        branch = args.branch or helper.get_current_branch()
        result = helper.push(remote=args.remote, branch=branch)
    elif args.action == 'branches':
        result = helper.get_branches()
    elif args.action == 'log':
        result = helper.log(max_count=args.count)
    else:
        print(f"未知操作: {args.action}")
        return
    
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(result['stdout'])
        if result['stderr']:
            print(f"错误: {result['stderr']}")


if __name__ == "__main__":
    main()
