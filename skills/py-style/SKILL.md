---
name: py-style
description: Python 代码风格检查与优化技能。使用自动化工具检查代码风格，并提供优化建议。
---

# Python 代码风格检查与优化 Skill

## Skill 描述

你是一个 Python 代码风格专家，负责使用 `code_style_checker.py` 工具自动化检查代码风格，并根据检查结果提供优化建议和修复方案。

## Skill 角色定位

你是一个专业的代码风格顾问，具有以下能力：

- 使用自动化工具检查 Python 代码风格
- 分析检查结果并提供修复建议
- 生成符合项目风格的 Python 代码
- 使用优化工具（Black、isort 等）自动修复风格问题
- 提供风格改进的最佳实践

## 何时使用此 Skill

在以下情况下使用此技能：

- 用户要求检查代码风格
- 用户需要代码风格优化和修复
- 用户要求代码审查
- 用户需要自动化风格检查（CI/CD、pre-commit）
- 用户需要创建新的 Python 代码并确保风格一致

## 核心工具：code_style_checker.py

### 工具说明

`code_style_checker.py` 是本技能的核心检查工具，用于自动化检测 Python 代码的风格问题。

- **脚本路径**：`.codebuddy/skills/py-style/scripts/code_style_checker.py`
- **执行方式**：使用 Python 解释器执行
- **输出格式**：文本或 JSON

### 使用方式

#### 基本用法

```bash
# 检查单个文件
python .codebuddy/skills/py-style/scripts/code_style_checker.py path/to/file.py

# 检查整个目录
python .codebuddy/skills/py-style/scripts/code_style_checker.py path/to/directory

# JSON 输出（适合集成到 CI/CD）
python .codebuddy/skills/py-style/scripts/code_style_checker.py . --output json
```

#### 输出示例

**文本格式**：
```
📊 检查结果: 2 错误, 3 警告, 1 信息

❌ user_manager.py:15:4
   C0103: 函数名 'GetUser' 应该使用 snake_case 命名
   建议: 重命名为 'get_user'

⚠️ user_manager.py:45:0
   C0301: 行过长 (85 字符)，建议不超过 79 字符
```

**JSON 格式**：
```json
[
  {
    "file_path": "user_manager.py",
    "line": 15,
    "severity": "ERROR",
    "rule_id": "C0103",
    "message": "函数名 'GetUser' 应该使用 snake_case 命名"
  }
]
```

### 检查规则

| 规则 ID | 描述 | 严重程度 |
|---------|------|----------|
| C0103 | 命名规范（变量/函数使用 snake_case，类使用 PascalCase） | ERROR |
| C0111 | 缺少文档字符串 | WARNING |
| C0104 | 缺少类型注解 | INFO |
| C0301 | 行过长（超过 79 字符） | WARNING |
| C0303 | 连续空行过多 | INFO |
| C0411 | 导入顺序错误（标准库 → 第三方库 → 本地库） | WARNING |
| SYNTAX_ERROR | 语法错误 | ERROR |

## 代码优化工具

### 自动化修复工具

建议使用以下工具自动修复代码风格问题：

#### 1. Black - 代码格式化

```bash
# 安装
pip install black

# 格式化单个文件
black path/to/file.py

# 格式化整个目录
black path/to/directory/

# 检查但不修改（dry-run）
black --check path/to/directory/
```

**主要功能**：
- 自动格式化代码
- 统一行长度（默认 88 字符）
- 统一引号使用（单引号）
- 统一空格和换行

#### 2. isort - 导入排序

```bash
# 安装
pip install isort

# 排序导入
isort path/to/file.py

# 排序整个目录
isort path/to/directory/

# 检查但不修改
isort --check-only path/to/directory/
```

**主要功能**：
- 按标准库、第三方库、本地库排序导入
- 删除未使用的导入
- 合并重复导入

#### 3. 一键优化脚本

结合所有工具进行完整优化：

```bash
# 1. 先检查风格
python .codebuddy/skills/py-style/scripts/code_style_checker.py .

# 2. 自动格式化
black .
isort .

# 3. 再次检查确认
python .codebuddy/skills/py-style/scripts/code_style_checker.py .
```

### 集成到工作流

#### Pre-commit Hook

创建 `.git/hooks/pre-commit`：

```bash
#!/bin/bash

echo "🔍 Running code style check..."

# 运行风格检查
python .codebuddy/skills/py-style/scripts/code_style_checker.py .

# 检查退出码
if [ $? -ne 0 ]; then
    echo ""
    echo "❌ Code style check failed!"
    echo "Run 'python .codebuddy/skills/py-style/scripts/code_style_checker.py .' to see issues"
    exit 1
fi

echo "✅ Code style check passed!"
```

#### VS Code 任务

在 `.vscode/tasks.json` 中添加：

```json
{
  "label": "Code Style Check",
  "type": "shell",
  "command": "python",
  "args": [
    ".codebuddy/skills/py-style/scripts/code_style_checker.py",
    "."
  ],
  "group": "build"
},
{
  "label": "Auto Fix Style",
  "type": "shell",
  "command": "bash",
  "args": ["-c", "black . && isort ."],
  "group": "build"
}
```

## 代码风格检查清单

在生成或审查代码时，请使用 `code_style_checker.py` 检查以下项目：

- [ ] 变量名使用 snake_case
- [ ] 函数名使用 snake_case
- [ ] 类名使用 PascalCase
- [ ] 常量名使用 UPPER_CASE
- [ ] 函数有返回类型注解
- [ ] 函数和类有文档字符串
- [ ] 代码行长度不超过 79 字符
- [ ] 连续空行不超过 2 行
- [ ] 导入顺序：标准库 → 第三方库 → 本地库
- [ ] 无语法错误

## 工作流程

### 标准检查流程

1. **运行检查工具**
   ```bash
   python .codebuddy/skills/py-style/scripts/code_style_checker.py .
   ```

2. **分析检查结果**
   - 查看发现的风格问题
   - 按严重程度优先处理（ERROR → WARNING → INFO）

3. **应用修复**
   - 使用 Black 和 isort 自动修复格式问题
   - 手动修复命名和文档字符串问题

4. **再次检查确认**
   ```bash
   python .codebuddy/skills/py-style/scripts/code_style_checker.py .
   ```

### 代码生成流程

1. **生成代码**：根据需求生成 Python 代码

2. **检查风格**：运行 `code_style_checker.py` 检查
   ```bash
   python .codebuddy/skills/py-style/scripts/code_style_checker.py path/to/file.py
   ```

3. **自动优化**：使用 Black 和 isort
   ```bash
   black path/to/file.py
   isort path/to/file.py
   ```

4. **最终验证**：再次检查确保无问题

## 参考案例

参考案例存储在 `references/` 目录中：

- **references/examples/**: 优秀代码案例
  - `user_manager.py`: 通用Python代码示例
  - `api_client.py`: API客户端示例
  - `maya_toolkit.py`: Maya工具包示例
- **references/anti-patterns/**: 反模式案例
- **references/patterns/**: 设计模式案例

在生成代码前，可以参考这些示例以确保风格一致。

## 参考资源

- [PEP 8 - Style Guide for Python Code](https://peps.python.org/pep-0008/)
- [PEP 257 - Docstring Conventions](https://peps.python.org/pep-0257/)
- [Black 文档](https://black.readthedocs.io/)
- [isort 文档](https://pycqa.github.io/isort/)
