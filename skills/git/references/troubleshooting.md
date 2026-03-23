# Git 故障排查指南

## 常见错误及解决方案

### 1. "fatal: not a git repository"

**问题描述**：在非 Git 仓库目录中执行 Git 命令

**原因**：当前目录不是 Git 仓库

**解决方案**：
```bash
# 方案1：初始化仓库
git init

# 方案2：切换到正确的仓库目录
cd /path/to/your/git/repository

# 方案3：克隆现有仓库
git clone <repository-url>
```

---

### 2. "error: failed to push some refs"

**问题描述**：推送时失败，提示远程仓库有本地没有的提交

**原因**：远程仓库有新的提交，与本地提交产生冲突

**解决方案**：
```bash
# 方案1：先拉取再推送
git pull origin main
git push origin main

# 方案2：使用 rebase 保持线性历史
git pull --rebase origin main
git push origin main

# 方案3：手动解决冲突后推送
git pull origin main
# 手动解决冲突文件
git add <conflicted-files>
git commit
git push origin main
```

---

### 3. "CONFLICT (content): Merge conflict"

**问题描述**：合并时产生冲突

**原因**：同一文件的同一行在不同分支中被修改

**解决方案**：
```bash
# 1. 查看冲突文件
git status

# 2. 打开冲突文件，会看到类似标记：
# <<<<<<< HEAD
# 你的代码
# =======
# 他们的代码
# >>>>>>> branch-name

# 3. 手动编辑解决冲突

# 4. 标记冲突已解决
git add <conflicted-files>

# 5. 提交合并
git commit

# 6. 如果要取消合并
git merge --abort
```

**可视化解决冲突工具**：
```bash
# 使用配置的差异工具
git mergetool

# 使用 VS Code
git config --global merge.tool vscode
git config --global mergetool.vscode.cmd 'code --wait $MERGED'
```

---

### 4. "fatal: refusing to merge unrelated histories"

**问题描述**：两个不相关的仓库尝试合并

**原因**：两个仓库有不同的历史记录

**解决方案**：
```bash
# 允许合并不相关历史
git pull origin main --allow-unrelated-histories

# 或者使用 rebase
git pull origin main --allow-unrelated-histories --rebase
```

---

### 5. "detached HEAD"

**问题描述**：处于分离头指针状态

**原因**：检出了特定的提交或标签，而不是分支

**解决方案**：
```bash
# 方案1：返回分支
git checkout main
# 或
git switch main

# 方案2：基于当前提交创建新分支
git checkout -b new-branch
# 或
git switch -c new-branch

# 方案3：如果丢失了提交，使用 reflog 找回
git reflog
git reset --hard HEAD@{n}
```

---

### 6. "error: src refspec main does not match any"

**问题描述**：推送时找不到指定的分支

**原因**：本地没有该分支，或分支名称拼写错误

**解决方案**：
```bash
# 检查本地分支
git branch

# 检查当前分支
git branch --show-current

# 创建并切换到 main 分支
git checkout -b main

# 如果是 master 分支
git branch -m master main

# 推送当前分支
git push -u origin $(git branch --show-current)
```

---

### 7. "fatal: remote origin already exists"

**问题描述**：添加远程仓库时，origin 已存在

**原因**：已经配置了名为 origin 的远程仓库

**解决方案**：
```bash
# 方案1：查看现有远程仓库
git remote -v

# 方案2：修改现有远程仓库的 URL
git remote set-url origin <new-url>

# 方案3：删除现有远程仓库
git remote remove origin
git remote add origin <url>

# 方案4：使用不同的名称
git remote add upstream <url>
```

---

### 8. "nothing added to commit but untracked files present"

**问题描述**：有未跟踪的文件但没有添加任何内容

**原因**：没有执行 `git add`，或文件在 `.gitignore` 中

**解决方案**：
```bash
# 方案1：添加所有文件
git add .

# 方案2：添加指定文件
git add <filename>

# 方案3：查看 .gitignore
cat .gitignore

# 方案4：强制添加被忽略的文件
git add -f <filename>

# 方案5：查看未跟踪文件
git status
git status --short
```

---

### 9. "fatal: refusing to merge unrelated histories"

**问题描述**：合并不相关的历史

**原因**：两个仓库有不同的历史记录

**解决方案**：
```bash
# 允许合并不相关历史
git pull origin main --allow-unrelated-histories

# 如果在 rebase 过程中
git rebase origin/main --allow-unrelated-histories
```

---

### 10. "error: Your local changes to the following files would be overwritten by checkout"

**问题描述**：切换分支时会覆盖本地修改

**原因**：工作区有未提交的修改

**解决方案**：
```bash
# 方案1：提交本地修改
git add .
git commit -m "Save changes"

# 方案2：暂存本地修改
git stash
git checkout <branch-name>
git stash pop

# 方案3：放弃本地修改
git checkout -- .
git checkout <branch-name>

# 方案4：强制切换（不推荐）
git checkout -f <branch-name>
```

---

### 11. "fatal: current branch 'feature' has no upstream branch"

**问题描述**：分支没有设置上游

**原因**：新分支没有关联远程分支

**解决方案**：
```bash
# 方案1：推送并设置上游
git push -u origin feature

# 方案2：推送后设置上游
git push origin feature
git branch --set-upstream-to=origin/feature feature

# 方案3：使用简写设置上游
git branch -u origin/feature
```

---

### 12. "Author identity unknown"

**问题描述**：提交时提示用户信息未配置

**原因**：没有配置用户名和邮箱

**解决方案**：
```bash
# 配置当前仓库
git config user.name "Your Name"
git config user.email "your.email@example.com"

# 配置全局（推荐）
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# 查看当前配置
git config user.name
git config user.email
```

---

### 13. "fatal: could not read Username"

**问题描述**：认证失败

**原因**：没有配置认证信息

**解决方案**：
```bash
# 方案1：使用 HTTPS 并输入用户名密码
git push origin main

# 方案2：使用 SSH 密钥
# 生成 SSH 密钥
ssh-keygen -t rsa -b 4096 -C "your.email@example.com"
# 添加到 ssh-agent
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_rsa
# 复制公钥到 GitHub/GitLab
cat ~/.ssh/id_rsa.pub

# 方案3：使用凭据缓存
git config --global credential.helper cache
git config --global credential.helper 'cache --timeout=3600'

# 方案4：使用凭据存储
git config --global credential.helper store
```

---

### 14. "fatal: bad signature"

**问题描述**：仓库损坏

**原因**：Git 对象数据库损坏

**解决方案**：
```bash
# 检查仓库完整性
git fsck

# 尝试恢复
git gc --prune=now

# 如果还有问题，重新克隆
git clone --no-hardlinks /path/to/corrupt/repo /path/to/new/repo
```

---

### 15. "fatal: unable to access 'https://github.com/...'"

**问题描述**：无法访问远程仓库

**原因**：网络问题、代理问题或 URL 错误

**解决方案**：
```bash
# 方案1：检查网络连接
ping github.com

# 方案2：检查 URL
git remote -v
git remote set-url origin <correct-url>

# 方案3：配置代理
git config --global http.proxy http://proxy-server:port
git config --global https.proxy https://proxy-server:port

# 取消代理
git config --global --unset http.proxy
git config --global --unset https.proxy

# 方案4：使用 SSH 替代 HTTPS
git remote set-url origin git@github.com:user/repo.git
```

---

### 16. "error: pathspec '...' did not match any file(s) known to git"

**问题描述**：指定的路径不匹配任何文件

**原因**：文件路径错误或文件不存在

**解决方案**：
```bash
# 方案1：检查文件是否存在
ls -la

# 方案2：使用 Tab 补全
git add <filename>

# 方案3：查看当前目录
pwd

# 方案4：使用通配符
git add *.py
git add **/*.py
```

---

### 17. "warning: ignoring broken ref refs/remotes/origin/..."

**问题描述**：远程引用损坏

**原因**：远程分支已删除但本地仍保留引用

**解决方案**：
```bash
# 清理远程分支引用
git remote prune origin

# 使用 fetch 时自动清理
git fetch --prune
git fetch -p

# 手动删除损坏的引用
cd .git/refs/remotes/origin
# 删除损坏的文件
```

---

### 18. "fatal: cannot open .git/FETCH_HEAD: Permission denied"

**问题描述**：权限问题

**原因**：文件或目录权限不足

**解决方案**：
```bash
# 方案1：修复权限（Linux/macOS）
sudo chown -R $(whoami) .git
chmod -R 755 .git

# 方案2：Windows 上检查文件属性
# 右键 .git 文件夹 -> 属性 -> 取消只读

# 方案3：删除 .git 文件夹中的锁文件
rm .git/index.lock
rm .git/refs/heads/main.lock
```

---

### 19. "error: cannot lock ref 'refs/heads/...': ..."

**问题描述**：无法锁定引用

**原因**：另一个 Git 进程正在运行或有残留锁文件

**解决方案**：
```bash
# 查找并删除锁文件
find .git -name "*.lock" -type f

# 删除锁文件
rm .git/HEAD.lock
rm .git/index.lock

# 如果还有问题，重启 Git 相关进程
# Windows
taskkill /F /IM git.exe
# Linux/macOS
killall git
```

---

### 20. 大文件问题

**问题描述**：推送大文件失败

**原因**：文件超过 GitHub/GitLab 的限制（通常 100MB）

**解决方案**：
```bash
# 方案1：使用 Git LFS
git lfs install
git lfs track "*.psd"
git lfs track "*.zip"
git add .gitattributes
git add .
git commit -m "Add LFS files"

# 方案2：从历史中删除大文件
git filter-branch --tree-filter 'rm -f large-file.zip' HEAD
git filter-repo --path large-file.zip --invert-paths

# 方案3：使用 BFG Repo-Cleaner
bfg --strip-blobs-bigger-than 100M
git reflog expire --expire=now --all
git gc --prune=now --aggressive
```

---

## 性能问题

### 仓库运行缓慢

**解决方案**：
```bash
# 清理和优化
git gc --aggressive --prune=now

# 清理不必要的文件
git clean -fd

# 检查仓库大小
du -sh .git

# 使用浅克隆
git clone --depth 1 <repository-url>

# 只克隆特定分支
git clone --single-branch --branch main <repository-url>
```

---

## 恢复丢失的提交

### 使用 reflog 恢复

```bash
# 查看操作历史
git reflog

# 恢复到指定状态
git reset --hard HEAD@{n}

# 恢复删除的分支
git branch recover-branch HEAD@{5}
```

---

## 查看详细信息

### 获取更多诊断信息

```bash
# 详细模式
git -v pull

# 跟踪执行过程
GIT_TRACE=1 git pull

# 查看配置
git config --list --show-origin

# 查看远程详细信息
git remote show origin
```

---

## 预防措施

### 1. 定期备份
```bash
# 创建备份分支
git branch backup-$(date +%Y%m%d)

# 推送备份到远程
git push origin backup-$(date +%Y%m%d)
```

### 2. 使用钩子
```bash
# 安装 pre-push 钩子防止误推送
cat > .git/hooks/pre-push << 'EOF'
#!/bin/sh
# 检查是否在 main 分支
if [ "$(git rev-parse --abbrev-ref HEAD)" = "main" ]; then
    echo "Warning: You are pushing to main branch!"
    read -p "Continue? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi
EOF
chmod +x .git/hooks/pre-push
```

### 3. 配置别名提高效率
```bash
# 添加常用别名
git config --global alias.st status
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.ci commit
git config --global alias.unstage 'reset HEAD --'
git config --global alias.last 'log -1 HEAD'
```

## 获取帮助

```bash
# 查看命令帮助
git help <command>
git <command> --help
man git-<command>

# 查看完整手册
git help --all

# 在线帮助
https://git-scm.com/docs
https://git-scm.com/book/zh/v2
```

---

**注意**：在执行任何危险操作（如 `git reset --hard`、`git clean`）之前，请确保：
1. 已提交当前工作
2. 或已创建备份分支
3. 或已使用 stash 保存工作
