#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Git Helper Script
提供 Git 操作的辅助功能
"""

import os
import sys
import subprocess
from pathlib import Path
from typing import List, Optional, Tuple, Dict


class GitHelper:
    """Git 辅助类"""

    def __init__(self, repo_path: Optional[str] = None):
        """
        初始化 GitHelper

        Args:
            repo_path: Git 仓库路径，默认为当前目录
        """
        self.repo_path = Path(repo_path) if repo_path else Path.cwd()
        self.git_path = self._find_git_executable()

    def _find_git_executable(self) -> str:
        """查找 Git 可执行文件"""
        try:
            result = subprocess.run(['which', 'git'], capture_output=True, text=True)
            if result.returncode == 0:
                return result.stdout.strip()
        except:
            pass

        # Windows 下尝试查找 git.exe
        if os.name == 'nt':
            possible_paths = [
                r'C:\Program Files\Git\bin\git.exe',
                r'C:\Program Files\Git\cmd\git.exe',
                r'C:\Program Files (x86)\Git\bin\git.exe',
            ]
            for path in possible_paths:
                if os.path.exists(path):
                    return path

        return 'git'

    def run_git_command(self, args: List[str]) -> Tuple[int, str, str]:
        """
        执行 Git 命令

        Args:
            args: Git 命令参数列表

        Returns:
            (returncode, stdout, stderr)
        """
        cmd = [self.git_path] + args
        try:
            result = subprocess.run(
                cmd,
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='replace'
            )
            return result.returncode, result.stdout.strip(), result.stderr.strip()
        except FileNotFoundError:
            return 1, "", f"Git not found at: {self.git_path}"
        except Exception as e:
            return 1, "", str(e)

    def is_git_repo(self) -> bool:
        """检查是否为 Git 仓库"""
        returncode, _, _ = self.run_git_command(['rev-parse', '--is-inside-work-tree'])
        return returncode == 0

    def get_status(self) -> Dict:
        """获取仓库状态"""
        if not self.is_git_repo():
            return {'error': 'Not a git repository'}

        returncode, stdout, _ = self.run_git_command(['status', '--porcelain'])

        if returncode != 0:
            return {'error': 'Failed to get status'}

        modified = []
        added = []
        deleted = []
        untracked = []
        renamed = []

        for line in stdout.split('\n'):
            if not line:
                continue
            status = line[:2]
            filepath = line[3:]

            if status == ' M':
                modified.append(filepath)
            elif status == 'M ':
                added.append(filepath)
            elif status == ' D':
                deleted.append(filepath)
            elif status == '??':
                untracked.append(filepath)
            elif status in ('R ', 'R '):
                renamed.append(filepath)

        return {
            'modified': modified,
            'added': added,
            'deleted': deleted,
            'untracked': untracked,
            'renamed': renamed
        }

    def get_current_branch(self) -> Optional[str]:
        """获取当前分支名"""
        if not self.is_git_repo():
            return None

        returncode, stdout, _ = self.run_git_command(['rev-parse', '--abbrev-ref', 'HEAD'])

        if returncode == 0:
            return stdout
        return None

    def get_branches(self) -> List[str]:
        """获取所有分支"""
        if not self.is_git_repo():
            return []

        returncode, stdout, _ = self.run_git_command(['branch'])
        branches = []

        if returncode == 0:
            for line in stdout.split('\n'):
                if line:
                    # 移除开头的 * 和空格
                    branch = line.replace('*', '').strip()
                    branches.append(branch)

        return branches

    def get_log(self, count: int = 10) -> List[Dict]:
        """获取提交历史"""
        if not self.is_git_repo():
            return []

        # 获取简洁的提交信息
        returncode, stdout, _ = self.run_git_command([
            'log', f'--oneline', '-{count}'
        ])

        commits = []

        if returncode == 0:
            for line in stdout.split('\n'):
                if line:
                    parts = line.split(' ', 1)
                    if len(parts) == 2:
                        commit_hash = parts[0]
                        message = parts[1]
                        commits.append({
                            'hash': commit_hash,
                            'message': message
                        })

        return commits

    def get_remotes(self) -> Dict[str, str]:
        """获取远程仓库"""
        if not self.is_git_repo():
            return {}

        returncode, stdout, _ = self.run_git_command(['remote', '-v'])

        remotes = {}

        if returncode == 0:
            for line in stdout.split('\n'):
                if line:
                    parts = line.split('\t')
                    if len(parts) == 2:
                        name = parts[0]
                        url = parts[1].split(' ')[0]
                        remotes[name] = url

        return remotes

    def add_files(self, files: List[str]) -> Tuple[int, str, str]:
        """添加文件到暂存区"""
        return self.run_git_command(['add'] + files)

    def commit(self, message: str) -> Tuple[int, str, str]:
        """提交更改"""
        return self.run_git_command(['commit', '-m', message])

    def create_branch(self, branch_name: str) -> Tuple[int, str, str]:
        """创建分支"""
        return self.run_git_command(['branch', branch_name])

    def checkout_branch(self, branch_name: str) -> Tuple[int, str, str]:
        """切换分支"""
        return self.run_git_command(['checkout', branch_name])

    def create_and_checkout_branch(self, branch_name: str) -> Tuple[int, str, str]:
        """创建并切换分支"""
        return self.run_git_command(['checkout', '-b', branch_name])

    def pull(self, remote: str = 'origin', branch: Optional[str] = None) -> Tuple[int, str, str]:
        """拉取远程更新"""
        if branch:
            return self.run_git_command(['pull', remote, branch])
        return self.run_git_command(['pull', remote])

    def push(self, remote: str = 'origin', branch: Optional[str] = None, upstream: bool = False) -> Tuple[int, str, str]:
        """推送到远程"""
        args = ['push']
        if upstream:
            args.append('-u')
        args.append(remote)
        if branch:
            args.append(branch)
        return self.run_git_command(args)

    def stash(self, message: str = '') -> Tuple[int, str, str]:
        """暂存工作进度"""
        if message:
            return self.run_git_command(['stash', 'save', message])
        return self.run_git_command(['stash'])

    def stash_list(self) -> List[Dict]:
        """查看暂存列表"""
        returncode, stdout, _ = self.run_git_command(['stash', 'list'])

        stashes = []

        if returncode == 0:
            for line in stdout.split('\n'):
                if line:
                    # 解析 stash@{n}: message
                    parts = line.split(': ', 1)
                    if len(parts) == 2:
                        stash_ref = parts[0]
                        message = parts[1]
                        stashes.append({
                            'ref': stash_ref,
                            'message': message
                        })

        return stashes

    def stash_pop(self, stash_ref: str = '') -> Tuple[int, str, str]:
        """恢复并删除暂存"""
        if stash_ref:
            return self.run_git_command(['stash', 'pop', stash_ref])
        return self.run_git_command(['stash', 'pop'])

    def stash_drop(self, stash_ref: str = '') -> Tuple[int, str, str]:
        """删除暂存"""
        if stash_ref:
            return self.run_git_command(['stash', 'drop', stash_ref])
        return self.run_git_command(['stash', 'drop'])

    def reset(self, mode: str = 'mixed', commit: str = 'HEAD~1') -> Tuple[int, str, str]:
        """
        重置到指定提交

        Args:
            mode: soft, mixed, hard
            commit: 提交引用
        """
        return self.run_git_command(['reset', f'--{mode}', commit])

    def revert(self, commit: str) -> Tuple[int, str, str]:
        """撤销提交"""
        return self.run_git_command(['revert', commit])

    def get_config(self, key: str, scope: str = '') -> Optional[str]:
        """
        获取配置

        Args:
            key: 配置键
            scope: 配置范围 (--global, --local, --system)
        """
        args = ['config']
        if scope:
            args.append(scope)
        args.append(key)

        returncode, stdout, _ = self.run_git_command(args)

        if returncode == 0:
            return stdout
        return None

    def set_config(self, key: str, value: str, scope: str = '') -> Tuple[int, str, str]:
        """
        设置配置

        Args:
            key: 配置键
            value: 配置值
            scope: 配置范围 (--global, --local, --system)
        """
        args = ['config']
        if scope:
            args.append(scope)
        args.append(key)
        args.append(value)

        return self.run_git_command(args)

    def get_tags(self) -> List[str]:
        """获取所有标签"""
        returncode, stdout, _ = self.run_git_command(['tag'])

        if returncode == 0:
            return [tag for tag in stdout.split('\n') if tag]
        return []

    def create_tag(self, tag_name: str, message: str = '') -> Tuple[int, str, str]:
        """创建标签"""
        if message:
            return self.run_git_command(['tag', '-a', tag_name, '-m', message])
        return self.run_git_command(['tag', tag_name])

    def delete_tag(self, tag_name: str, remote: str = '') -> Tuple[int, str, str]:
        """删除标签"""
        if remote:
            return self.run_git_command(['push', remote, '--delete', tag_name])
        return self.run_git_command(['tag', '-d', tag_name])

    def check_conflicts(self) -> List[str]:
        """检查是否有冲突"""
        returncode, stdout, _ = self.run_git_command(['diff', '--name-only', '--diff-filter=U'])

        if returncode == 0:
            return [file for file in stdout.split('\n') if file]
        return []

    def get_unmerged_files(self) -> List[str]:
        """获取未合并的文件"""
        returncode, stdout, _ = self.run_git_command(['ls-files', '-u'])

        if returncode == 0:
            files = set()
            for line in stdout.split('\n'):
                if line:
                    parts = line.split()
                    if len(parts) >= 4:
                        files.add(parts[3])
            return list(files)
        return []


def main():
    """命令行入口"""
    import argparse

    parser = argparse.ArgumentParser(description='Git Helper Script')
    parser.add_argument('--path', help='Git repository path')
    parser.add_argument('--status', action='store_true', help='Show git status')
    parser.add_argument('--branch', action='store_true', help='Show current branch')
    parser.add_argument('--branches', action='store_true', help='Show all branches')
    parser.add_argument('--log', type=int, nargs='?', const=10, help='Show commit history')
    parser.add_argument('--remotes', action='store_true', help='Show remote repositories')
    parser.add_argument('--tags', action='store_true', help='Show all tags')
    parser.add_argument('--config', help='Get git config value')
    parser.add_argument('--conflicts', action='store_true', help='Check for conflicts')

    args = parser.parse_args()

    git = GitHelper(args.path)

    if args.status:
        status = git.get_status()
        print("Git Status:")
        if 'error' in status:
            print(f"  Error: {status['error']}")
        else:
            if status['modified']:
                print(f"  Modified: {', '.join(status['modified'])}")
            if status['added']:
                print(f"  Added: {', '.join(status['added'])}")
            if status['deleted']:
                print(f"  Deleted: {', '.join(status['deleted'])}")
            if status['untracked']:
                print(f"  Untracked: {', '.join(status['untracked'])}")
            if not any(status.values()):
                print("  Working directory clean")

    if args.branch:
        branch = git.get_current_branch()
        print(f"Current branch: {branch}")

    if args.branches:
        branches = git.get_branches()
        print("Branches:")
        for branch in branches:
            current = '*' if branch == git.get_current_branch() else ' '
            print(f"  {current} {branch}")

    if args.log:
        commits = git.get_log(args.log)
        print(f"Recent commits (last {args.log}):")
        for commit in commits:
            print(f"  {commit['hash'][:8]} {commit['message']}")

    if args.remotes:
        remotes = git.get_remotes()
        print("Remote repositories:")
        for name, url in remotes.items():
            print(f"  {name}: {url}")

    if args.tags:
        tags = git.get_tags()
        print("Tags:")
        for tag in tags:
            print(f"  {tag}")

    if args.config:
        value = git.get_config(args.config)
        print(f"{args.config}: {value}")

    if args.conflicts:
        conflicts = git.check_conflicts()
        if conflicts:
            print("Conflicts found in:")
            for file in conflicts:
                print(f"  {file}")
        else:
            print("No conflicts found")


if __name__ == '__main__':
    main()
