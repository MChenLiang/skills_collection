# Git Skill 完整说明

## 概述

这是一个完整的 Git 版本控制系统 Skill，包含了从基础到高级的所有 Git 知识和实用工具。

## 目录结构

```
git/
├── SKILL.md                      # Skill 主文档（YAML front matter + 完整知识库）
├── README.md                     # 本文件
├── references/                   # 参考文档目录
│   ├── commands.md              # Git 命令完整参考手册
│   └── troubleshooting.md       # Git 故障排查指南
└── scripts/                      # 实用脚本目录
    ├── git_helper.py            # Git 辅助工具（Python）
    └── README.md                # 脚本使用说明
```

## 文件说明

### 1. SKILL.md (13.82 KB)

Skill 的核心文档，包含：

- **Skill 元数据**：YAML front matter（name, description）
- **核心知识**：完整 Git 知识体系
  - 基本概念（工作区、暂存区、版本库）
  - 命令分类（仓库管理、提交修改、分支管理、远程操作等）
  - Git Flow 工作流
  - 高级操作（交互式暂存、Stash、Rebase、Cherry-Pick）
  - 配置与安装
  - 服务器搭建
- **使用指南**：何时使用、如何响应、命令执行原则
- **常见场景**：8个实用工作流程
- **最佳实践**：提交规范、分支策略、安全注意事项
- **故障排查**：5个常见问题及解决方案
- **参考资源**：官方文档链接

### 2. references/commands.md (10.22 KB)

Git 命令完整参考手册，包含：

- **仓库操作**：init, clone, status
- **配置管理**：config 查看和设置
- **添加与提交**：add, commit, log
- **分支操作**：branch, checkout, switch, merge, cherry-pick
- **合并与变基**：merge, rebase, cherry-pick
- **远程操作**：remote, fetch, pull, push
- **标签操作**：tag 查看、创建、推送、删除
- **撤销操作**：checkout, reset, revert, reflog
- **Stash 操作**：stash 保存、查看、应用、删除
- **查看差异**：diff 各种用法
- **查看历史**：log, blame, show
- **其他常用命令**：clean, grep, ls-tree 等
- **Git Flow 工作流命令**
- **常见工作流程**：5个完整示例
- **.gitignore 文件示例**
- **Git 配置别名**
- **SSH 密钥配置**

### 3. references/troubleshooting.md (11.5 KB)

Git 故障排查指南，包含 20+ 个常见问题：

- "fatal: not a git repository"
- "error: failed to push some refs"
- "CONFLICT (content): Merge conflict"
- "detached HEAD"
- "error: src refspec main does not match any"
- "fatal: refusing to merge unrelated histories"
- "fatal: remote origin already exists"
- "nothing added to commit but untracked files present"
- "Author identity unknown"
- "fatal: could not read Username"
- "fatal: bad signature"
- "fatal: unable to access"
- "error: pathspec '...' did not match"
- 权限问题、大文件问题、性能问题

每个问题都包含：
- 问题描述
- 原因分析
- 详细解决方案（多个方案）
- 相关命令和技巧

额外包含：
- 恢复丢失的提交
- 获取诊断信息
- 预防措施
- 获取帮助的方法

### 4. scripts/git_helper.py (13.8 KB)

Python 实现的 Git 辅助工具，提供：

#### GitHelper 类

**仓库检查**
- `is_git_repo()` - 检查是否为 Git 仓库

**状态管理**
- `get_status()` - 获取仓库状态（修改、新增、删除、未跟踪）
- `check_conflicts()` - 检查冲突
- `get_unmerged_files()` - 获取未合并文件

**分支操作**
- `get_current_branch()` - 获取当前分支
- `get_branches()` - 获取所有分支
- `create_branch()` - 创建分支
- `checkout_branch()` - 切换分支
- `create_and_checkout_branch()` - 创建并切换分支

**提交历史**
- `get_log()` - 获取提交历史

**远程仓库**
- `get_remotes()` - 获取远程仓库列表

**文件操作**
- `add_files()` - 添加文件到暂存区
- `commit()` - 提交更改

**暂存操作**
- `stash()` - 保存工作进度
- `stash_list()` - 查看暂存列表
- `stash_pop()` - 恢复并删除暂存
- `stash_drop()` - 删除暂存

**推送和拉取**
- `pull()` - 拉取远程更新
- `push()` - 推送到远程

**重置和撤销**
- `reset()` - 重置到指定提交（soft/mixed/hard）
- `revert()` - 撤销提交

**配置管理**
- `get_config()` - 获取配置
- `set_config()` - 设置配置

**标签管理**
- `get_tags()` - 获取所有标签
- `create_tag()` - 创建标签
- `delete_tag()` - 删除标签

#### 命令行接口

```bash
python scripts/git_helper.py --status
python scripts/git_helper.py --branch
python scripts/git_helper.py --branches
python scripts/git_helper.py --log [count]
python scripts/git_helper.py --remotes
python scripts/git_helper.py --tags
python scripts/git_helper.py --config key
python scripts/git_helper.py --conflicts
python scripts/git_helper.py --path /path/to/repo --status
```

### 5. scripts/README.md (7.86 KB)

脚本使用说明文档，包含：

- 功能特性列表
- 安装依赖说明
- 使用方式（Python 模块 + 命令行）
- 完整的 API 参考
- 4 个实用示例：
  1. 完整的 Git 工作流
  2. 检查和解决冲突
  3. 批量操作
  4. 获取项目信息
- 错误处理示例
- 注意事项
- 扩展和自定义指南

## 使用方式

### 1. 作为 Skill 使用

当用户询问 Git 相关问题时，系统会自动加载这个 Skill，提供：

- 详细的命令说明
- 最佳实践建议
- 故障排查方案
- 完整的工作流程

### 2. 使用 Python 脚本

```python
from scripts.git_helper import GitHelper

# 初始化
git = GitHelper('/path/to/repo')

# 使用各种功能
status = git.get_status()
branch = git.get_current_branch()
commits = git.get_log(count=10)
```

### 3. 命令行工具

```bash
# 查看状态
python scripts/git_helper.py --status

# 查看分支
python scripts/git_helper.py --branches

# 查看日志
python scripts/git_helper.py --log 20
```

### 4. 查阅参考文档

- 命令参考：`references/commands.md`
- 故障排查：`references/troubleshooting.md`

## 特点

### ✅ 完整性

- 覆盖 Git 的所有核心概念和命令
- 从基础到高级的完整知识体系
- 包含 100+ 个实用命令示例

### ✅ 实用性

- Python 脚本可直接使用
- 命令行工具支持快速操作
- 完整的 API 文档和示例

### ✅ 可靠性

- 详细的故障排查指南
- 20+ 常见问题解决方案
- 最佳实践建议

### ✅ 易用性

- 清晰的文档结构
- 丰富的代码示例
- 逐步的操作指南

## 适用场景

1. **初始化新项目**：从零开始设置 Git 仓库
2. **日常开发**：提交、分支、合并等日常操作
3. **团队协作**：远程仓库、Pull Request、代码审查
4. **问题排查**：解决冲突、恢复丢失的提交
5. **自动化**：使用 Python 脚本自动化 Git 操作
6. **学习参考**：完整的 Git 知识库和命令手册

## 技术特点

### 跨平台支持

- 支持 Windows、Linux、macOS
- 自动检测 Git 可执行文件路径
- 正确处理路径分隔符

### 健壮性

- 完善的错误处理
- 返回值包含详细信息
- 异常捕获和处理

### 可扩展性

- 基于 GitHelper 类可轻松扩展
- 支持自定义工具和工作流
- 模块化设计

## 版本信息

- **创建日期**：2025-02-28
- **文档版本**：1.0
- **Git 版本**：兼容 Git 2.0+
- **Python 版本**：支持 Python 3.6+

## 维护和更新

如需更新或扩展这个 Skill：

1. **更新知识库**：修改 `SKILL.md`
2. **添加新命令**：更新 `references/commands.md`
3. **记录新问题**：添加到 `references/troubleshooting.md`
4. **扩展功能**：修改 `scripts/git_helper.py`
5. **更新文档**：同步更新 `scripts/README.md`

## 反馈和贡献

如果你发现问题或有改进建议，欢迎反馈！

---

**享受使用 Git，让版本控制变得更简单！** 🚀
