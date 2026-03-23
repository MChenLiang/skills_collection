# Git Scripts 目录说明

本目录包含 Git 操作的辅助脚本，用于自动化和简化常见的 Git 操作。

## 脚本列表

### 1. git_helper.py

Git 辅助工具，提供 Python API 和命令行接口。

#### 功能特性

- ✅ 仓库状态检查
- ✅ 分支管理（查看、创建、切换）
- ✅ 提交历史查询
- ✅ 远程仓库管理
- ✅ 暂存（stash）操作
- ✅ 配置管理
- ✅ 标签管理
- ✅ 冲突检测
- ✅ 重置和撤销

#### 安装依赖

```bash
# Python 3.6+
python --version

# 无需额外依赖，使用标准库
```

#### 使用方式

##### 作为 Python 模块使用

```python
from scripts.git_helper import GitHelper

# 初始化
git = GitHelper('/path/to/repo')

# 检查是否为 Git 仓库
if git.is_git_repo():
    print("This is a Git repository")

# 获取状态
status = git.get_status()
print(f"Modified files: {status['modified']}")
print(f"Untracked files: {status['untracked']}")

# 获取当前分支
branch = git.get_current_branch()
print(f"Current branch: {branch}")

# 获取所有分支
branches = git.get_branches()
print(f"All branches: {branches}")

# 获取提交历史
commits = git.get_log(count=5)
for commit in commits:
    print(f"{commit['hash'][:8]} - {commit['message']}")

# 获取远程仓库
remotes = git.get_remotes()
for name, url in remotes.items():
    print(f"{name}: {url}")

# 获取配置
username = git.get_config('user.name')
email = git.get_config('user.email')
print(f"User: {username} <{email}>")

# 检查冲突
conflicts = git.check_conflicts()
if conflicts:
    print(f"Conflicts in: {conflicts}")
```

##### 命令行使用

```bash
# 显示仓库状态
python scripts/git_helper.py --status

# 显示当前分支
python scripts/git_helper.py --branch

# 显示所有分支
python scripts/git_helper.py --branches

# 显示最近 10 条提交
python scripts/git_helper.py --log

# 显示最近 20 条提交
python scripts/git_helper.py --log 20

# 显示远程仓库
python scripts/git_helper.py --remotes

# 显示所有标签
python scripts/git_helper.py --tags

# 获取配置值
python scripts/git_helper.py --config user.name
python scripts/git_helper.py --config user.email

# 检查冲突
python scripts/git_helper.py --conflicts

# 指定仓库路径
python scripts/git_helper.py --path /path/to/repo --status
```

#### API 参考

##### GitHelper 类

**初始化**
```python
git = GitHelper(repo_path='/path/to/repo')
```

**仓库检查**
```python
git.is_git_repo()  # bool
```

**状态管理**
```python
git.get_status()  # Dict: {modified, added, deleted, untracked, renamed}
```

**分支操作**
```python
git.get_current_branch()  # str or None
git.get_branches()  # List[str]
git.create_branch('feature-name')  # (returncode, stdout, stderr)
git.checkout_branch('feature-name')  # (returncode, stdout, stderr)
git.create_and_checkout_branch('feature-name')  # (returncode, stdout, stderr)
```

**提交历史**
```python
git.get_log(count=10)  # List[Dict]: [{hash, message}]
```

**远程仓库**
```python
git.get_remotes()  # Dict: {name: url}
```

**文件操作**
```python
git.add_files(['file1.txt', 'file2.txt'])  # (returncode, stdout, stderr)
git.commit('Commit message')  # (returncode, stdout, stderr)
```

**暂存操作**
```python
git.stash('Work in progress')  # (returncode, stdout, stderr)
git.stash_list()  # List[Dict]: [{ref, message}]
git.stash_pop()  # (returncode, stdout, stderr)
git.stash_drop('stash@{0}')  # (returncode, stdout, stderr)
```

**推送和拉取**
```python
git.pull('origin', 'main')  # (returncode, stdout, stderr)
git.push('origin', 'main', upstream=True)  # (returncode, stdout, stderr)
```

**重置和撤销**
```python
git.reset('soft', 'HEAD~1')  # (returncode, stdout, stderr)
git.revert('abc123')  # (returncode, stdout, stderr)
```

**配置管理**
```python
git.get_config('user.name')  # str or None
git.set_config('user.name', 'Your Name')  # (returncode, stdout, stderr)
git.set_config('user.name', 'Your Name', '--global')  # (returncode, stdout, stderr)
```

**标签管理**
```python
git.get_tags()  # List[str]
git.create_tag('v1.0.0', 'Release 1.0.0')  # (returncode, stdout, stderr)
git.delete_tag('v1.0.0')  # (returncode, stdout, stderr)
git.delete_tag('v1.0.0', 'origin')  # (returncode, stdout, stderr)
```

**冲突检测**
```python
git.check_conflicts()  # List[str]
git.get_unmerged_files()  # List[str]
```

## 使用示例

### 示例 1：完整的 Git 工作流

```python
from scripts.git_helper import GitHelper

git = GitHelper('/path/to/project')

# 1. 检查状态
status = git.get_status()
if status['untracked']:
    print(f"Untracked files: {status['untracked']}")

# 2. 添加文件
git.add_files(['new_file.py', 'updated_file.py'])

# 3. 提交
git.commit('Add new features')

# 4. 创建功能分支
git.create_and_checkout_branch('feature/new-feature')

# 5. 推送到远程
git.push('origin', 'feature/new-feature', upstream=True)
```

### 示例 2：检查和解决冲突

```python
from scripts.git_helper import GitHelper

git = GitHelper('/path/to/project')

# 拉取最新代码
code, out, err = git.pull('origin', 'main')

# 检查冲突
conflicts = git.check_conflicts()
if conflicts:
    print(f"Conflicts found in: {conflicts}")
    # 提示用户手动解决冲突
    # 解决后添加文件
    git.add_files(conflicts)
    # 提交合并
    git.commit('Resolve merge conflicts')
else:
    print("No conflicts")
```

### 示例 3：批量操作

```python
from scripts.git_helper import GitHelper

git = GitHelper('/path/to/project')

# 查看所有分支
branches = git.get_branches()
print("All branches:", branches)

# 切换到每个分支并拉取最新代码
for branch in branches:
    print(f"Processing branch: {branch}")
    git.checkout_branch(branch)
    git.pull('origin', branch)

# 切换回主分支
git.checkout_branch('main')
```

### 示例 4：获取项目信息

```python
from scripts.git_helper import GitHelper

git = GitHelper('/path/to/project')

# 收集项目信息
info = {
    'is_git_repo': git.is_git_repo(),
    'current_branch': git.get_current_branch(),
    'all_branches': git.get_branches(),
    'recent_commits': git.get_log(count=5),
    'remotes': git.get_remotes(),
    'status': git.get_status(),
    'tags': git.get_tags(),
    'user': {
        'name': git.get_config('user.name'),
        'email': git.get_config('user.email')
    }
}

import json
print(json.dumps(info, indent=2))
```

## 错误处理

```python
from scripts.git_helper import GitHelper

git = GitHelper('/path/to/project')

# 检查命令执行结果
code, stdout, stderr = git.commit('Test commit')
if code != 0:
    print(f"Error: {stderr}")
    if stderr:
        # 处理错误
        pass
else:
    print("Success: ", stdout)

# 捕获异常
try:
    branch = git.get_current_branch()
    if branch:
        print(f"On branch: {branch}")
except Exception as e:
    print(f"An error occurred: {e}")
```

## 注意事项

1. **路径处理**：脚本使用绝对路径和跨平台路径处理
2. **编码处理**：使用 UTF-8 编码处理 Git 输出
3. **错误处理**：所有 Git 命令都返回 (returncode, stdout, stderr) 元组
4. **性能**：频繁的 Git 命令调用可能会影响性能，建议批量操作
5. **安全性**：脚本不会修改用户的 Git 配置，除非明确调用 `set_config`

## 扩展和自定义

你可以基于 `GitHelper` 类创建自己的工具：

```python
from scripts.git_helper import GitHelper

class MyGitTool(GitHelper):
    def deploy(self, branch='main'):
        """部署流程"""
        # 切换到主分支
        self.checkout_branch(branch)
        # 拉取最新代码
        self.pull('origin', branch)
        # 获取最新版本
        tags = self.get_tags()
        if tags:
            latest_tag = tags[-1]
            print(f"Latest version: {latest_tag}")
        return True

# 使用
tool = MyGitTool('/path/to/project')
tool.deploy()
```

## 许可证

此脚本随 Git Skill 一起提供，可自由使用和修改。
