# 代码风格检查工具

## 概述

`code_style_checker.py` 是一个自动化的 Python 代码风格检查工具，用于确保代码符合项目的编码规范。

## 功能特性

### 检查项目

1. **命名规范检查**
   - 变量名使用 snake_case
   - 函数名使用 snake_case
   - 类名使用 PascalCase
   - 常量名使用 UPPER_CASE

2. **文档字符串检查**
   - 函数是否有文档字符串
   - 类是否有文档字符串

3. **类型注解检查**
   - 函数是否有返回类型注解
   - 参数类型注解（基础检查）

4. **代码格式检查**
   - 行长度（不超过 79 字符）
   - 连续空行（不超过 2 行）
   - 导入顺序（标准库 → 第三方库 → 本地库）

5. **语法错误检查**
   - 检测 Python 语法错误

## 安装

无需额外安装，使用 Python 标准库：

```bash
python --version  # Python 3.6+
```

## 使用方式

### 基本用法

```bash
# 检查单个文件
python code_style_checker.py path/to/file.py

# 检查整个目录
python code_style_checker.py path/to/directory

# 检查当前目录
python code_style_checker.py .
```

### 输出格式

#### 文本格式（默认）

```bash
python code_style_checker.py file.py
```

输出示例：

```
📊 检查结果: 2 错误, 3 警告, 1 信息

❌ user_manager.py:15:4
   C0103: 函数名 'GetUser' 应该使用 snake_case 命名
   建议: 重命名为 'get_user'

⚠️ user_manager.py:45:0
   C0301: 行过长 (85 字符)，建议不超过 79 字符

ℹ️ user_manager.py:78:4
   C0104: 函数 'updateUser' 缺少返回类型注解
```

#### JSON 格式

```bash
python code_style_checker.py file.py --output json
```

输出示例：

```json
[
  {
    "file_path": "user_manager.py",
    "line": 15,
    "column": 4,
    "severity": "ERROR",
    "rule_id": "C0103",
    "message": "函数名 'GetUser' 应该使用 snake_case 命名",
    "suggestion": "重命名为 'get_user'"
  },
  {
    "file_path": "user_manager.py",
    "line": 45,
    "column": 0,
    "severity": "WARNING",
    "rule_id": "C0301",
    "message": "行过长 (85 字符)，建议不超过 79 字符",
    "suggestion": null
  }
]
```

### 命令行选项

```bash
python code_style_checker.py [选项] <路径>

选项:
  --output, -o {text,json}  输出格式 (默认: text)
  path                    文件或目录路径
```

## 检查规则

### C0103: 命名规范

**严重程度**: ERROR

**描述**: 变量、函数、类名不符合命名规范

**示例**:
```python
# ❌ 错误
userName = "John"        # 变量使用驼峰
def GetUser():           # 函数使用大写开头
class user_manager:      # 类使用小写

# ✅ 正确
user_name = "John"       # 变量使用 snake_case
def get_user():          # 函数使用 snake_case
class UserManager:       # 类使用 PascalCase
```

### C0111: 缺少文档字符串

**严重程度**: WARNING

**描述**: 函数或类缺少文档字符串

**示例**:
```python
# ❌ 错误
def get_user(user_id):
    return db.query(user_id)

# ✅ 正确
def get_user(user_id: int) -> Optional[Dict]:
    """
    获取用户信息

    Args:
        user_id: 用户 ID

    Returns:
        用户信息字典
    """
    return db.query(user_id)
```

### C0104: 缺少类型注解

**严重程度**: INFO

**描述**: 函数缺少返回类型注解

**示例**:
```python
# ❌ 缺少类型注解
def get_user(user_id):
    pass

# ✅ 有类型注解
def get_user(user_id: int) -> Optional[Dict]:
    pass
```

### C0301: 行过长

**严重程度**: WARNING

**描述**: 代码行超过 79 字符

**示例**:
```python
# ❌ 行过长
result = some_very_long_function_name(with_many, arguments, that_make, the, line, too, long)

# ✅ 使用括号换行
result = some_very_long_function_name(
    with_many, arguments, that_make, the, line, too, long
)
```

### C0303: 连续空行过多

**严重程度**: INFO

**描述**: 连续超过 2 个空行

**示例**:
```python
# ❌ 连续 3 个空行
def func1():
    pass



def func2():
    pass

# ✅ 最多 2 个空行
def func1():
    pass


def func2():
    pass
```

### C0411: 导入顺序错误

**严重程度**: WARNING

**描述**: 导入顺序不正确（应该是：标准库 → 第三方库 → 本地库）

**示例**:
```python
# ❌ 顺序错误
from local_module import func
import os
import requests

# ✅ 正确顺序
import os

import requests

from local_module import func
```

### SYNTAX_ERROR: 语法错误

**严重程度**: ERROR

**描述**: Python 语法错误

**示例**:
```python
# ❌ 语法错误
def func(
    print("hello"  # 缺少右括号

# ✅ 正确
def func():
    print("hello")
```

## 扩展和自定义

### 添加新的检查规则

在 `CodeStyleChecker` 类中添加新的检查方法：

```python
def _check_custom_rule(self, file_path: str, lines: List[str]) -> None:
    """
    自定义检查规则

    Args:
        file_path: 文件路径
        lines: 行列表
    """
    for line_no, line in enumerate(lines, 1):
        # 实现你的检查逻辑
        if 'TODO' in line and 'TODO:' not in line:
            self.issues.append(StyleIssue(
                file_path=file_path,
                line=line_no,
                column=line.find('TODO'),
                severity=Severity.INFO,
                rule_id="CUSTOM1",
                message="TODO 应该使用 'TODO:' 格式"
            ))
```

然后在 `check_file` 方法中调用：

```python
def check_file(self, file_path: str) -> List[StyleIssue]:
    self.issues = []

    # ... 其他检查 ...

    # 自定义检查
    self._check_custom_rule(file_path, lines)

    return self.issues
```

### 修改检查规则

调整现有检查的严重程度或规则：

```python
# 修改行长度限制
def _check_line_length(self, file_path: str, lines: List[str]) -> None:
    for line_no, line in enumerate(lines, 1):
        if len(line) > 88:  # 从 79 改为 88
            self.issues.append(...)
```

### 添加排除规则

在初始化方法中添加要排除的目录或文件：

```python
def __init__(self, project_root: Optional[str] = None):
    self.project_root = Path(project_root) if project_root else Path.cwd()
    self.issues: List[StyleIssue] = []
    self._excluded_dirs = {
        '.git', '__pycache__', '.venv', 'venv',
        'node_modules', 'build', 'dist',
        'tests',  # 添加 tests 目录
    }
```

## 集成到项目

### Pre-commit Hook

创建 `.git/hooks/pre-commit`：

```bash
#!/bin/bash

echo "Running code style check..."

# 运行检查
python .codebuddy/skills/py-style/scripts/code_style_checker.py .

# 检查退出码
if [ $? -ne 0 ]; then
    echo ""
    echo "❌ Code style check failed!"
    echo "Please fix the issues before committing."
    exit 1
fi

echo "✅ Code style check passed!"
```

赋予执行权限：

```bash
chmod +x .git/hooks/pre-commit
```

### Makefile 集成

在 Makefile 中添加：

```makefile
# 代码风格检查
style-check:
    @echo "Running code style check..."
    @python .codebuddy/skills/py-style/scripts/code_style_checker.py .

# 自动修复（如果需要）
style-fix:
    @echo "Auto-fixing code style..."
    @black .
    @isort .
```

### VS Code 任务

在 `.vscode/tasks.json` 中添加：

```json
{
    "version": "2.0.0",
    "tasks": [
        {
            "label": "Code Style Check",
            "type": "shell",
            "command": "python",
            "args": [
                ".codebuddy/skills/py-style/scripts/code_style_checker.py",
                "."
            ],
            "group": "build",
            "presentation": {
                "reveal": "always",
                "panel": "new"
            }
        }
    ]
}
```

## 性能优化

### 并行检查

对于大型项目，可以使用多进程并行检查：

```python
from multiprocessing import Pool

def check_file_parallel(self, file_path: str) -> List[StyleIssue]:
    """并行检查文件"""
    with Pool() as pool:
        results = pool.map(self.check_file, file_paths)
    return [issue for issues in results for issue in issues]
```

### 缓存结果

缓存检查结果以提高性能：

```python
import hashlib
import json
from pathlib import Path

def _get_file_hash(self, file_path: str) -> str:
    """获取文件哈希"""
    with open(file_path, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()

def _check_cached(self, file_path: str) -> Optional[List[StyleIssue]]:
    """检查缓存"""
    cache_file = Path('.code_style_cache.json')
    if not cache_file.exists():
        return None

    file_hash = self._get_file_hash(file_path)
    cache = json.loads(cache_file.read_text())

    return cache.get(file_hash)
```

## 故障排查

### 问题：检查器报错 "No module named 'typing'"

**解决方案**：升级 Python 到 3.6+，typing 在 Python 3.6+ 中是标准库。

### 问题：检查结果不准确

**解决方案**：
1. 确保 Python 文件语法正确
2. 检查是否有编码问题
3. 更新到最新版本的检查器

### 问题：性能太慢

**解决方案**：
1. 使用排除规则跳过不需要检查的目录
2. 使用并行检查（需要修改代码）
3. 只检查修改过的文件

## 参考资源

- [PEP 8 - Style Guide for Python Code](https://peps.python.org/pep-0008/)
- [PEP 257 - Docstring Conventions](https://peps.python.org/pep-0257/)
- [pylint](https://pylint.pycqa.org/)
- [flake8](https://flake8.pycqa.org/)

## 许可证

本工具随 Code Style Skill 一起提供，可自由使用和修改。
