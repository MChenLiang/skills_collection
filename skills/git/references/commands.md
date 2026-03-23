# Git 参考文档

本文档包含 Git 的详细参考信息和最佳实践指南。

## Git 命令速查表

### 仓库操作

```bash
# 初始化新仓库
git init

# 克隆仓库
git clone <repository-url>
git clone <repository-url> <directory-name>

# 查看仓库状态
git status
git status -s  # 简短格式
```

### 配置管理

```bash
# 查看配置
git config --list
git config user.name
git config user.email

# 设置用户信息（当前仓库）
git config user.name "Your Name"
git config user.email "your.email@example.com"

# 设置用户信息（全局）
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# 编辑配置文件
git config -e
git config -e --global

# 设置编辑器
git config --global core.editor "code --wait"
git config --global core.editor "vim"

# 设置差异工具
git config --global merge.tool vimdiff
```

### 添加与提交

```bash
# 添加文件到暂存区
git add <filename>
git add .
git add *.txt
git add -A  # 添加所有更改（包括删除）

# 交互式添加
git add -p  # 逐块选择

# 提交更改
git commit -m "Commit message"
git commit -am "Commit message"  # 添加并提交已跟踪文件

# 修改最后一次提交
git commit --amend -m "New message"
git commit --amend --no-edit  # 只修改内容，不修改消息

# 查看提交历史
git log
git log --oneline
git log --graph
git log --graph --oneline --all
git log --stat
git log -p
git log -n 5
git log --author="Author Name"
git log --since="2024-01-01"
git log --until="2024-12-31"
git log --grep="keyword"
```

### 分支操作

```bash
# 查看分支
git branch
git branch -r  # 远程分支
git branch -a  # 所有分支
git branch --merged
git branch --no-merged

# 创建分支
git branch <branch-name>
git checkout -b <branch-name>  # 创建并切换
git switch -c <branch-name>     # Git 2.23+

# 切换分支
git checkout <branch-name>
git switch <branch-name>       # Git 2.23+

# 删除分支
git branch -d <branch-name>    # 已合并的分支
git branch -D <branch-name>    # 强制删除

# 重命名分支
git branch -m <old-name> <new-name>

# 查看分支信息
git show-branch
git show-branch --all
```

### 合并与变基

```bash
# 合并分支
git merge <branch-name>
git merge --no-ff <branch-name>  # 保留合并历史
git merge --abort  # 取消合并

# 变基
git rebase <branch-name>
git rebase -i HEAD~3  # 交互式变基
git rebase --continue
git rebase --abort
git rebase --skip

# 拣选提交
git cherry-pick <commit-hash>
git cherry-pick <commit1> <commit2>
git cherry-pick <start>..<end>
git cherry-pick -n <commit>  # 应用但不提交
git cherry-pick --continue
git cherry-pick --abort
```

### 远程操作

```bash
# 查看远程仓库
git remote -v
git remote show <remote-name>

# 添加远程仓库
git remote add <name> <url>
git remote add origin https://github.com/user/repo.git

# 删除远程仓库
git remote remove <name>
git remote rm <name>

# 重命名远程仓库
git remote rename <old-name> <new-name>

# 修改远程仓库 URL
git remote set-url <name> <new-url>

# 获取远程更新
git fetch
git fetch <remote-name>
git fetch --prune  # 清理已删除的远程分支

# 拉取并合并
git pull
git pull <remote-name> <branch-name>
git pull --rebase

# 推送到远程
git push
git push <remote-name> <branch-name>
git push -u origin main  # 设置上游分支
git push --all
git push --tags
git push --delete <branch-name>  # 删除远程分支
```

### 标签操作

```bash
# 列出标签
git tag
git tag -l "v1.*"

# 创建标签
git tag v1.0.0
git tag -a v1.0.0 -m "Version 1.0.0"
git tag -s v1.0.0 -m "Signed tag"

# 查看标签信息
git show v1.0.0

# 推送标签
git push origin v1.0.0
git push origin --tags

# 删除标签
git tag -d v1.0.0
git push origin --delete v1.0.0

# 检出标签
git checkout v1.0.0
```

### 撤销操作

```bash
# 撤销工作区更改
git checkout -- <filename>
git restore <filename>  # Git 2.23+

# 撤销暂存区更改
git reset HEAD <filename>
git restore --staged <filename>  # Git 2.23+

# 重置到指定提交
git reset --soft HEAD~1    # 保留更改在暂存区
git reset --mixed HEAD~1   # 取消暂存（默认）
git reset --hard HEAD~1    # 丢弃所有更改

# 撤销提交（创建新提交）
git revert <commit-hash>

# 查看操作历史
git reflog
git reflog show HEAD
git reset --hard HEAD@{5}  # 恢复到指定状态
```

### Stash 操作

```bash
# 保存工作进度
git stash
git stash save "message"
git stash -u  # 包括未跟踪的文件

# 查看存储列表
git stash list

# 应用存储
git stash apply
git stash apply stash@{0}

# 应用并删除存储
git stash pop
git stash pop stash@{0}

# 查看存储内容
git stash show
git stash show -p
git stash show -p stash@{0}

# 删除存储
git stash drop
git stash drop stash@{0}
git stash clear  # 清空所有存储

# 从存储创建分支
git stash branch <branch-name> stash@{0}
```

### 查看差异

```bash
# 查看工作区与暂存区差异
git diff
git diff <filename>

# 查看暂存区与提交差异
git diff --cached
git diff --staged

# 查看工作区与指定提交差异
git diff HEAD
git diff HEAD~1
git diff <commit-hash>

# 查看两个提交之间差异
git diff <commit1> <commit2>
git diff HEAD~3 HEAD

# 查看分支差异
git diff master feature
git diff master..feature

# 查看统计信息
git diff --stat
git diff --stat HEAD~1
```

### 查看历史

```bash
# 查看提交历史
git log
git log --oneline
git log --graph
git log --graph --all --oneline

# 查看文件修改历史
git log --follow <filename>
git log --patch <filename>
git log --all --full-history <filename>

# 查看文件每一行的修改者
git blame <filename>
git blame -L 10,20 <filename>  # 查看指定行

# 查找包含特定内容的提交
git log -S "search string"
git log -G "regex pattern"

# 查看提交详情
git show <commit-hash>
git show HEAD
git show HEAD~1
git show v1.0.0
```

### 其他常用命令

```bash
# 清理未跟踪文件
git clean -f
git clean -fd  # 包括目录
git clean -fX  # 只删除 .gitignore 中指定的文件

# 搜索文件内容
git grep "pattern"
git grep -i "pattern"
git grep "pattern" -- "*.py"

# 查看对象
git ls-tree HEAD
git ls-files
git ls-remote

# 归档仓库
git archive --format=zip --output=project.zip HEAD

# 统计信息
git shortlog
git shortlog -sn  # 按提交者统计

# 显示描述信息
git describe
git describe --tags
git describe --all
```

## Git Flow 工作流

### 初始化
```bash
git flow init
```

### 功能分支
```bash
git flow feature start <feature-name>
git flow feature finish <feature-name>
git flow feature publish <feature-name>
git flow feature pull <feature-name>
```

### 发布分支
```bash
git flow release start <release-version>
git flow release finish <release-version>
git flow release publish <release-version>
```

### 修复分支
```bash
git flow hotfix start <hotfix-version>
git flow hotfix finish <hotfix-version>
git flow hotfix publish <hotfix-version>
```

### 支持分支
```bash
git flow support start <support-version> <base-branch>
git flow support finish <support-version>
```

## 常见工作流程

### 1. 开始新项目
```bash
# 创建目录并初始化
mkdir my-project
cd my-project
git init

# 添加文件
git add .

# 首次提交
git commit -m "Initial commit"

# 添加远程仓库
git remote add origin https://github.com/user/repo.git

# 推送到远程
git push -u origin main
```

### 2. 开发新功能
```bash
# 更新主分支
git checkout main
git pull origin main

# 创建功能分支
git checkout -b feature/new-feature

# 开发并提交
git add .
git commit -m "Add new feature"

# 推送功能分支
git push -u origin feature/new-feature

# 创建 Pull Request
# 在 GitHub/GitLab 上创建 PR

# 合并后清理
git checkout main
git pull origin main
git branch -d feature/new-feature
git push origin --delete feature/new-feature
```

### 3. 修复紧急问题
```bash
# 从 main 创建修复分支
git checkout main
git pull origin main
git checkout -b hotfix/urgent-fix

# 修复并提交
git add .
git commit -m "Fix urgent issue"

# 推送并合并
git push -u origin hotfix/urgent-fix
# 创建并合并 PR

# 回到 main 并更新
git checkout main
git pull origin main

# 合并到 develop（如果有）
git checkout develop
git merge main
git push origin develop

# 清理
git branch -d hotfix/urgent-fix
```

### 4. 解决合并冲突
```bash
# 拉取最新代码
git pull origin main

# 如果有冲突
git status  # 查看冲突文件

# 手动编辑冲突文件
# 解决冲突并保存

# 标记冲突已解决
git add <conflicted-files>

# 提交合并
git commit
git push origin main
```

### 5. 使用 Stash 切换任务
```bash
# 保存当前工作
git stash save "Work in progress"

# 切换到其他分支
git checkout other-branch

# 完成其他工作

# 切换回来
git checkout original-branch

# 恢复工作
git stash pop
```

## .gitignore 文件示例

```gitignore
# 操作系统
.DS_Store
Thumbs.db

# IDE
.vscode/
.idea/
*.swp
*.swo

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
.venv/

# Node.js
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*
dist/
build/

# Git
.git/

# 环境变量
.env
.env.local
.env.*.local

# 日志
*.log
logs/

# 临时文件
*.tmp
*.temp
temp/
```

## Git 配置别名

```bash
# 常用别名
git config --global alias.st status
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.ci commit
git config --global alias.unstage 'reset HEAD --'
git config --global alias.last 'log -1 HEAD'
git config --global alias.visual '!gitk'

# 查看所有别名
git config --global alias.lla 'log --graph --oneline --all'

# 使用别名
git st  # 等同于 git status
git co main  # 等同于 git checkout main
```

## SSH 密钥配置

```bash
# 生成 SSH 密钥
ssh-keygen -t rsa -b 4096 -C "your.email@example.com"

# 启动 ssh-agent
eval "$(ssh-agent -s)"

# 添加密钥到 ssh-agent
ssh-add ~/.ssh/id_rsa

# 查看公钥
cat ~/.ssh/id_rsa.pub

# 测试连接
ssh -T git@github.com
ssh -T git@gitlab.com
```

## 参考资源

- [Git 官方文档](https://git-scm.com/doc)
- [Pro Git Book](https://git-scm.com/book/zh/v2)
- [GitHub Flow](https://guides.github.com/introduction/flow/)
- [Git Flow](https://nvie.com/posts/a-successful-git-branching-model/)
- [Git 命令手册](https://git-scm.com/docs)
