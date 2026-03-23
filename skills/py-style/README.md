# Code Style Skill - Python 代码风格约束

## 概述

这是一个用于约束和检查 Python 代码风格的 Skill，支持 **3 种代码风格规范**，确保生成的代码符合不同场景的编码规范。

## 支持的代码风格

### 1. Web 后端 / FastAPI 风格 ⭐ 推荐
**适用场景**：Web 后端、API 开发、数据库操作
**参考来源**：`E:\working\website\backend\source` 项目

**主要特点**：
- ✅ FastAPI + Pydantic + pymysql 技术栈
- ✅ `__future__` 导入确保 Python 2/3 兼容性
- ✅ 统一错误处理装饰器模式 `@success`
- ✅ JWT 认证和签名验证
- ✅ 模块化日志记录
- ✅ `(bool, result/message)` 返回值规范
- ✅ Pydantic（API）vs Dataclass（内部）数据模型

### 2. Maya 工具包风格
**适用场景**：DCC 工具、Maya 插件开发
**参考来源**：`E:\working\working_coding\maya\tools\coding\CurveRig` 项目

**主要特点**：
- ✅ Maya 特定的撤销/重试装饰器 `@undoable`
- ✅ 中文错误消息
- ✅ 节点操作前验证
- ✅ 自定义异常类

### 3. 通用 Python 风格
**适用场景**：通用工具、数据处理、脚本开发
**参考来源**：PEP 8 标准规范

**主要特点**：
- ✅ 标准 PEP 8 规范
- ✅ 类型注解、文档字符串
- ✅ 异常处理、日志记录

## 目录结构

```
py-style/
├── SKILL.md                              (35 KB)   # Skill 主文档（3种风格规范）
├── README.md                             (本文件)  # 完整说明文档
├── QUICKSTART.md                         # 快速开始指南
├── references/                           # 参考案例目录
│   ├── examples/                        # 优秀代码案例
│   │   ├── web_backend.py              # Web后端示例（新增）⭐
│   │   ├── user_manager.py             # 用户管理器示例
│   │   ├── api_client.py               # API 客户端示例
│   │   └── maya_toolkit.py             # Maya工具包示例
│   ├── anti-patterns/                  # 反模式案例
│   │   └── bad_examples.py             # 不推荐的代码风格
│   └── maya_style_guide.md             # Maya代码风格指南
└── scripts/                             # 工具脚本目录
    ├── code_style_checker.py           # 代码风格检查工具
    └── README.md                       # 工具使用说明
```

## 功能特性

### 1. 代码风格规范

#### 命名规范
- ✅ 变量使用 snake_case
- ✅ 常量使用 UPPER_CASE
- ✅ 函数使用 snake_case
- ✅ 类使用 PascalCase
- ✅ 模块使用小写字母

#### 代码结构
- ✅ 正确的导入顺序（标准库 → 第三方库 → 本地库）
- ✅ 类和函数文档字符串
- ✅ 类型注解
- ✅ 适当的空行和缩进

#### 最佳实践
- ✅ 避免魔法数字和字符串
- ✅ 使用数据类
- ✅ 异常处理
- ✅ 日志记录
- ✅ 设计模式应用

### 2. 参考案例

#### 优秀案例（examples/）

1. **web_backend.py** - Web 后端示例 ⭐ **新增**
   - FastAPI + Pydantic + pymysql 技术栈
   - `__future__` 导入和分隔线注释
   - MySQL 数据库操作类
   - JWT 认证和签名验证
   - 装饰器模式 `@success`
   - 文件上传和分块合并
   - 单例日志类
   - Pydantic vs Dataclass 数据模型对比

2. **user_manager.py** - 用户管理器
   - 完整的类结构
   - 类型注解
   - 文档字符串
   - 异常处理
   - 日志记录

3. **api_client.py** - API 客户端
   - 上下文管理器
   - 重试机制
   - 错误处理
   - 数据类使用
   - 枚举类型

4. **maya_toolkit.py** - Maya工具包
   - Maya特定代码风格
   - Python 2/3兼容性处理
   - @undoable装饰器使用
   - 中文错误消息
   - Maya节点操作
   - 资源清理和atexit使用
   - property装饰器验证

#### 反模式案例（anti-patterns/）

**bad_examples.py** 展示了 10 个常见反模式：

1. 不规范的命名
2. 缺少类型注解
3. 魔法数字和字符串
4. 过长的函数
5. 过度的嵌套
6. 捕获所有异常
7. 重复代码
8. 不必要的注释
9. 硬编码配置
10. 过深的继承

每个反模式都有对应的推荐写法。

### 3. Maya代码风格指南

**references/maya_style_guide.md** 提供Maya相关代码的详细风格规范：

#### 核心特点

- **文件头规范**：标准化的文件头格式和分隔线
- **Python 2/3兼容**：future导入和版本检测
- **Maya装饰器**：@undoable和@success装饰器
- **错误处理**：使用中文错误消息和自定义异常
- **资源管理**：atexit和上下文管理器
- **Maya特定**：节点操作、属性创建、关节方向等

#### 适用场景

当需要生成以下类型的代码时参考此指南：

- Maya插件开发
- 绑定工具开发
- 自动化脚本
- DCC工具开发

### 4. 代码风格检查工具

**scripts/code_style_checker.py** 提供自动化检查功能：

#### 检查项目

- ❌ 命名规范（变量、函数、类）
- ❌ 缺少文档字符串
- ❌ 缺少类型注解
- ❌ 行长度（超过 79 字符）
- ❌ 连续空行过多
- ❌ 导入顺序错误

#### 使用方式

```bash
# 检查单个文件
python scripts/code_style_checker.py path/to/file.py

# 检查整个目录
python scripts/code_style_checker.py path/to/directory

# JSON 格式输出
python scripts/code_style_checker.py path/to/file.py --output json
```

#### 输出示例

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

## 使用方式

### 1. 作为 Skill 使用

当系统生成 Python 代码时，会自动应用本 Skill 的风格规范：

```python
# 生成的代码会遵循以下规范：
from typing import List, Dict, Optional

def get_user(user_id: int) -> Optional[Dict]:
    """
    获取用户信息

    Args:
        user_id: 用户 ID

    Returns:
        用户信息字典
    """
    pass
```

### 2. 学习参考案例

参考 `references/examples/` 目录中的优秀代码：

```python
# 学习 user_manager.py
- 类结构设计
- 方法组织
- 异常处理
- 日志记录

# 学习 api_client.py
- 上下文管理器
- 重试机制
- 数据类使用
- 枚举类型
```

### 3. 对比反模式

查看 `references/anti-patterns/` 避免常见错误：

```python
# 对比学习
# ❌ 反模式
userName = "John"  # 驼峰命名

# ✅ 推荐
user_name = "John"  # snake_case
```

### 4. 运行检查工具

定期运行检查工具：

```bash
# 检查整个项目
python .codebuddy/skills/py-style/scripts/code_style_checker.py .

# 检查特定文件
python .codebuddy/skills/py-style/scripts/code_style_checker.py src/main.py
```

## 代码风格检查清单

在生成或审查代码时，请确保：

### 命名规范
- [ ] 变量使用 snake_case
- [ ] 常量使用 UPPER_CASE
- [ ] 函数使用 snake_case
- [ ] 类使用 PascalCase
- [ ] 模块使用小写字母

### 类型注解
- [ ] 函数参数有类型注解
- [ ] 函数返回值有类型注解
- [ ] 使用了适当的类型（List, Dict, Optional 等）

### 文档字符串
- [ ] 模块有文档字符串
- [ ] 类有文档字符串
- [ ] 所有公开方法有文档字符串
- [ ] 遵循 Google 风格或 NumPy 风格

### 代码结构
- [ ] 导入顺序正确（标准库 → 第三方库 → 本地库）
- [ ] 类成员顺序正确（属性 → 属性方法 → 公开方法 → 私有方法）
- [ ] 函数长度适中（通常不超过 50 行）
- [ ] 嵌套层级不超过 4 层

### 最佳实践
- [ ] 避免魔法数字，使用常量
- [ ] 使用数据类（dataclass）
- [ ] 使用上下文管理器处理资源
- [ ] 捕获具体异常，而不是 Exception
- [ ] 添加适当的日志记录
- [ ] 使用适当的设计模式

## 扩展自定义

### 添加新的参考案例

在 `references/examples/` 添加新的优秀代码：

```python
"""
新模块文档字符串
"""

from typing import List, Dict

class NewClass:
    """新类文档字符串"""

    def method(self, param: int) -> str:
        """
        方法文档字符串

        Args:
            param: 参数

        Returns:
            返回值
        """
        pass
```

### 添加新的反模式

在 `references/anti-patterns/` 添加新的反模式：

```python
# ❌ 反模式
# 不推荐的写法

# ✅ 推荐
# 推荐的写法
```

### 自定义检查规则

修改 `scripts/code_style_checker.py` 添加新的检查规则：

```python
def _check_custom_rule(self, file_path: str, lines: List[str]) -> None:
    """自定义检查规则"""
    # 实现你的检查逻辑
    pass
```

## 集成到工作流

### Pre-commit Hook

在 `.git/hooks/pre-commit` 添加：

```bash
#!/bin/bash
echo "Running code style check..."
python .codebuddy/skills/py-style/scripts/code_style_checker.py .
if [ $? -ne 0 ]; then
    echo "❌ Code style check failed. Please fix the issues before committing."
    exit 1
fi
echo "✅ Code style check passed!"
```

### CI/CD 集成

在 CI 配置中添加：

```yaml
- name: Code Style Check
  run: |
    python .codebuddy/skills/py-style/scripts/code_style_checker.py .
```

## 工具对比

本 Skill 提供的工具与知名工具对比：

| 功能 | 本工具 | pylint | flake8 | mypy |
|------|--------|--------|--------|------|
| 命名检查 | ✅ | ✅ | ✅ | ❌ |
| 类型注解 | ✅ | ✅ | ❌ | ✅ |
| 文档字符串 | ✅ | ✅ | ❌ | ❌ |
| 行长度 | ✅ | ✅ | ✅ | ❌ |
| 导入顺序 | ✅ | ✅ | ✅ | ❌ |
| 静态类型检查 | ❌ | ❌ | ❌ | ✅ |
| 复杂度分析 | ❌ | ✅ | ✅ | ❌ |

**建议**：结合多个工具使用以获得最佳效果。

## 参考资源

- [PEP 8 - Style Guide for Python Code](https://peps.python.org/pep-0008/)
- [PEP 257 - Docstring Conventions](https://peps.python.org/pep-0257/)
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
- [Black - The Uncompromising Code Formatter](https://github.com/psf/black)
- [isort - Python import sorter](https://pycqa.github.io/isort/)

## 维护和更新

### 定期任务

- [ ] 添加新的参考案例
- [ ] 更新反模式案例
- [ ] 改进检查工具
- [ ] 更新文档

### 反馈和改进

如果发现问题或有改进建议：

1. 在 `references/examples/` 添加新的优秀案例
2. 在 `references/anti-patterns/` 添加新的反模式
3. 改进 `scripts/code_style_checker.py` 的检查规则
4. 更新 `SKILL.md` 的规范说明

## 许可证

本 Skill 随项目一起提供，可自由使用和修改。

---

**开始使用 Code Style Skill，让你的 Python 代码更加优雅！** ✨
