# Code Style Skill 快速开始

## 📁 目录结构

```
py-style/
├── SKILL.md                          (35 KB)   - Skill 主文档（包含3种风格规范）
├── README.md                         (8.03 KB)  - 完整说明文档
├── QUICKSTART.md                     (本文件)   - 快速开始指南
├── references/
│   ├── examples/                     # 优秀代码案例
│   │   ├── user_manager.py          (9.63 KB)  - 用户管理器示例
│   │   ├── api_client.py            (9.98 KB)  - API 客户端示例
│   │   └── maya_toolkit.py          (22.66 KB) - Maya工具包示例
│   ├── anti-patterns/                # 反模式案例
│   │   └── bad_examples.py          (9.32 KB)  - 不推荐的代码风格
│   └── maya_style_guide.md          (14.75 KB) - Maya代码风格指南
└── scripts/
    ├── code_style_checker.py        (16.3 KB)  - 代码风格检查工具
    └── README.md                    (9.34 KB)  - 工具使用说明
```

## 🚀 立即开始使用

### 1. 查阅 Skill 文档

```bash
cat .codebuddy/skills/py-style/SKILL.md
```

### 2. 学习优秀案例

```bash
# Web 后端示例（推荐）⭐
cat .codebuddy/skills/py-style/references/examples/web_backend.py

# 用户管理器示例
cat .codebuddy/skills/py-style/references/examples/user_manager.py

# API 客户端示例
cat .codebuddy/skills/py-style/references/examples/api_client.py

# Maya 工具包示例
cat .codebuddy/skills/py-style/references/examples/maya_toolkit.py
```

### 3. 对比反模式

```bash
cat .codebuddy/skills/py-style/references/anti-patterns/bad_examples.py
```

### 4. 运行代码风格检查

```bash
# 检查整个项目
python .codebuddy/skills/py-style/scripts/code_style_checker.py .

# 检查特定文件
python .codebuddy/skills/py-style/scripts/code_style_checker.py src/main.py

# JSON 格式输出
python .codebuddy/skills/py-style/scripts/code_style_checker.py . --output json
```

## 📚 主要内容

### SKILL.md (35 KB)

完整的代码风格规范，包含 3 种风格：

#### 1. Web 后端 / FastAPI 风格
- ✅ **文件头规范**：`__future__` 导入、分隔线注释
- ✅ **导入顺序**：标准库 → 第三方库 → 本地模块
- ✅ **装饰器模式**：`@success`、`@simple_success`
- ✅ **返回值规范**：`(bool, result/message)` 统一格式
- ✅ **数据模型**：Pydantic（API） vs Dataclass（内部）
- ✅ **数据库操作**：property 管理、私有方法
- ✅ **认证授权**：JWT、签名验证
- ✅ **日志记录**：logging 模块、级别管理
- ✅ **文件操作**：pathlib、aiofiles、分块读取

#### 2. Maya 工具包风格
- ✅ **文件头规范**：特殊注释分隔线
- ✅ **Python 2/3 兼容性**：future 导入、版本检测
- ✅ **装饰器使用**：`@undoable`、`@success`
- ✅ **中文错误消息**：assert、raise、print
- ✅ **类属性使用**：类属性、property 验证
- ✅ **资源清理**：atexit、__del__

#### 3. 通用 Python 风格
- ✅ **命名规范**：变量、常量、函数、类、模块命名
- ✅ **代码结构**：文件结构、类结构、导入顺序
- ✅ **类型注解**：基本类型、复杂类型、类型别名
- ✅ **文档字符串**：模块、类、函数文档字符串（Google 风格）
- ✅ **代码格式化**：行长度、空行、空格使用
- ✅ **异常处理**：捕获特定异常、finally 使用、上下文管理器
- ✅ **设计模式**：单例、工厂、策略模式
- ✅ **单元测试风格**：setUp/tearDown、测试方法命名
- ✅ **最佳实践**：类型注解、数据类、避免魔法数字
- ✅ **检查清单**：15+ 项检查清单

### references/examples/user_manager.py (9.63 KB)

完整的用户管理器实现，展示：

- ✅ 数据类（@dataclass）
- ✅ 自定义异常
- ✅ 完整的类结构
- ✅ 所有方法都有类型注解
- ✅ Google 风格文档字符串
- ✅ 异常处理
- ✅ 日志记录
- ✅ 私有方法（下划线开头）
- ✅ 静态方法
- ✅ 类方法

### references/examples/api_client.py (9.98 KB)

完整的 API 客户端实现，展示：

- ✅ 枚举类型
- ✅ 数据类
- ✅ 自定义异常
- ✅ 上下文管理器（__enter__/__exit__）
- ✅ 重试机制
- ✅ 错误处理
- ✅ 类型注解
- ✅ 文档字符串
- ✅ 常量定义

### references/anti-patterns/bad_examples.py (9.32 KB)

10 个常见反模式对比：

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

每个反模式都有 ❌ 错误示例和 ✅ 正确示例。

### scripts/code_style_checker.py (16.3 KB)

自动化代码风格检查工具，支持：

- ✅ 命名规范检查
- ✅ 文档字符串检查
- ✅ 类型注解检查
- ✅ 行长度检查
- ✅ 空行检查
- ✅ 导入顺序检查
- ✅ 语法错误检查
- ✅ 文本和 JSON 输出
- ✅ 排除目录和文件

## 🎯 使用场景

### 场景 1：生成 Web 后端代码

系统会自动应用 FastAPI 代码风格规范：

```python
#!/usr/bin/env python
# -*- coding:UTF-8 -*-

# +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+ #
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import logging
from typing import List, Dict, Any, Optional

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class UserService:
    """用户服务类"""

    def __init__(self, db_connection):
        self._db = db_connection
        logger.info("用户服务初始化完成")

    @property
    def db(self):
        return self._db

    def get_user(self, user_id: int) -> Optional[Dict[str, Any]]:
        """
        获取用户信息

        Args:
            user_id: 用户 ID

        Returns:
            用户信息字典，如果不存在返回 None
        """
        try:
            result = self._db.query(f"SELECT * FROM users WHERE id = {user_id}")
            logger.info(f"成功获取用户 {user_id}")
            return result
        except Exception as e:
            logger.error(f"获取用户失败: {e}", exc_info=True)
            return None
```

### 场景 2：生成 Maya 工具代码

系统会自动应用 Maya 工具包风格规范：

```python
#!/usr/bin/env python
# -*- coding:UTF-8 -*-

# +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+ #
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import maya.cmds as cmds
from functools import wraps

def undoable(func):
    """添加 Maya 撤销记录的装饰器"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        cmds.undoInfo(openChunk=True)
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(u"执行失败: {}".format(e))
            raise e
        finally:
            cmds.undoInfo(closeChunk=True)

    return wrapper

@undoable
def create_joint(name: str) -> str:
    """
    创建关节

    Args:
        name: 关节名称

    Returns:
        创建的关节名称
    """
    if cmds.objExists(name):
        raise RuntimeError(u"关节已存在: {}".format(name))
    return cmds.joint(name=name)
```

### 场景 3：学习最佳实践

参考优秀案例学习：

- Web 后端：`references/examples/user_manager.py`
- Maya 工具：`references/examples/maya_toolkit.py`
- API 客户端：`references/examples/api_client.py`

### 场景 4：避免常见错误

对比反模式避免：

- 不规范的命名
- 缺少类型注解
- 魔法数字
- 过度嵌套

### 场景 5：自动检查代码

运行检查工具：

```bash
python .codebuddy/skills/py-style/scripts/code_style_checker.py .
```

## 📋 检查清单

在生成或审查代码时，确保：

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
- [ ] 类成员顺序正确
- [ ] 函数长度适中
- [ ] 嵌套层级不超过 4 层

### 最佳实践

- [ ] 避免魔法数字，使用常量
- [ ] 使用数据类（dataclass）
- [ ] 使用上下文管理器处理资源
- [ ] 捕获具体异常
- [ ] 添加适当的日志记录

## 🔧 集成到工作流

### Pre-commit Hook

```bash
# 创建 .git/hooks/pre-commit
cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash
python .codebuddy/skills/py-style/scripts/code_style_checker.py .
if [ $? -ne 0 ]; then
    echo "❌ Code style check failed!"
    exit 1
fi
EOF
chmod +x .git/hooks/pre-commit
```

### VS Code 任务

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
      "group": "build"
    }
  ]
}
```

## 📖 参考资源

- [PEP 8 - Style Guide for Python Code](https://peps.python.org/pep-0008/)
- [PEP 257 - Docstring Conventions](https://peps.python.org/pep-0257/)
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)

## 🎉 开始使用

现在你可以：

1. **生成代码**：系统会自动应用代码风格规范
2. **学习案例**：参考 `references/examples/` 中的优秀代码
3. **对比学习**：查看 `references/anti-patterns/` 中的反模式
4. **自动检查**：使用 `scripts/code_style_checker.py` 检查代码

**让 Python 代码更加优雅和一致！** ✨
