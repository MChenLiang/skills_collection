# Maya工具包集成总结

## 概述

基于 `E:\working\working_coding\maya\tools\coding\CurveRig` 的maya工具包的代码风格规范。

## 新增内容

### 1. Maya工具包示例代码

**文件**: `references/examples/maya_toolkit.py` (22.63 KB)

包含以下完整示例：

- 自定义异常类（RigError, NodeNotFoundError, ValidationError）
- Maya装饰器（@undoable, @success）
- Maya工具函数（attr_num, attr_float, attr_int, attr_bool）
- 曲线工具类（CurveTool）
- 关节工具类（JointTool）
- 绑定构建器（RigBuilder）
- 验证函数
- 完整的文档字符串和类型注解

### 2. Maya代码风格指南

**文件**: `references/maya_style_guide.md` (14.86 KB)

详细说明：

#### 2.1 文件结构规范

- 标准文件头格式
- 导入顺序（future导入 → 第三方库 → 标准库 → 项目内部）
- 分隔线使用规范

#### 2.2 Python 2/3 兼容性

- future导入使用
- 版本检测模式
- reload处理
- DEVNULL兼容处理

#### 2.3 Maya特定风格

- 自定义异常定义
- undoable装饰器（所有修改场景的函数必须使用）
- success装饰器（用于处理成功/失败状态）
- Maya工具函数（属性创建、节点操作、命名函数）
- 类定义风格（类属性、property装饰器）
- Qt类定义风格

#### 2.4 命名规范

- Maya特定命名（_jnt, _ctrl, grp_, _crv等）
- 私有属性使用下划线前缀

#### 2.5 文档字符串

- Google风格文档字符串
- 包含Args、Returns、Raises、Examples

#### 2.6 错误处理

- 使用中文错误消息
- 异常捕获和处理模式
- assert验证使用

#### 2.7 注释风格

- 分隔线使用
- 行内注释规范

#### 2.8 最佳实践

- 资源清理（atexit、__del__）
- property验证
- Maya节点锁定/解锁

#### 2.9 完整示例

- Maya工具模块模板

#### 2.10 检查清单

- 生成Maya代码时的10项检查清单

### 3. SKILL.md 更新

在 SKILL.md 中添加了：

- Maya工具包参考案例说明
- Maya风格特点总结（6大特点）
- 文件头规范示例
- Python 2/3兼容性处理示例
- 装饰器使用示例
- Maya专用函数风格示例
- 错误消息使用中文说明
- 类属性使用示例

### 4. README.md 更新

更新了目录结构说明，新增：

- `maya_toolkit.py` 示例说明
- `maya_style_guide.md` 指南说明
- Maya代码风格指南章节

## 工具包代码风格特点总结

### 1. 文件头格式

```python
#!/usr/bin/env python
# -*- coding:UTF-8 -*-

# +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+ #
# 功能描述
# +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+ #
```

### 2. Python 2/3 兼容性

```python
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

_PY_3_ = sys.version_info.major > 2
if _PY_3_:
    from importlib import reload
    from subprocess import DEVNULL
else:
    DEVNULL = open(os.devnull, 'wb')
```

### 3. 装饰器使用

```python
@undoable
def create_joint(name):
    """添加撤销记录"""
    cmds.joint(name=name)


@success(show_error=True, show_success=True)
def build_rig(self):
    """处理成功/失败"""
    pass
```

### 4. 中文错误消息

```python
assert cmds.objExists(value), KeyError(u"没有找到根骨骼：%s" % value)
print(u"执行成功！\n{}".format(result))
```

### 5. 类属性使用

```python
class RigBuilder(object):
    dy_top_grp = "dyn_chains_ws_grp"
    dy_out_c_grp = "dyn_chains_out_c_grp"
```

### 6. Property验证

```python
@property
def root_jnt(self) -> str:
    return self._root_jnt


@root_jnt.setter
def root_jnt(self, value: str):
    assert cmds.objExists(value), KeyError(u"没有找到根骨骼：%s" % value)
    self._root_jnt = value
```

## 最终文件结构

```
py-style/
├── SKILL.md                              (18.34 KB) - Skill 主文档（已更新）
├── README.md                             (9.09 KB)  - 说明文档（已更新）
├── QUICKSTART.md                         (6.7 KB)   - 快速开始指南
├── references/
│   ├── examples/
│   │   ├── user_manager.py             (9.63 KB)  - 用户管理器示例
│   │   ├── api_client.py               (9.98 KB)  - API客户端示例
│   │   └── maya_toolkit.py            (22.63 KB) - Maya工具包示例（新增）
│   ├── anti-patterns/
│   │   └── bad_examples.py            (9.32 KB)  - 反模式示例
│   └── maya_style_guide.md            (14.86 KB)  - Maya风格指南（新增）
└── scripts/
    ├── code_style_checker.py          (16.3 KB)  - 检查工具
    └── README.md                      (9.34 KB)  - 工具说明
```

## 使用方式

### 1. 生成Maya相关代码时

系统会自动参考 `maya_toolkit.py` 示例，生成符合以下规范的代码：

- ✅ 标准文件头格式
- ✅ Python 2/3兼容性处理
- ✅ 使用@undoable装饰器
- ✅ 中文错误消息
- ✅ 类型注解和文档字符串
- ✅ Maya特定命名规范
- ✅ 资源清理处理

### 2. 查阅风格指南

```bash
# 查看Maya代码风格指南
cat .codebuddy/skills/py-style/references/maya_style_guide.md

# 查看Maya工具包示例
cat .codebuddy/skills/py-style/references/examples/maya_toolkit.py
```

### 3. 运行代码风格检查

```bash
# 检查整个项目
python .codebuddy/skills/py-style/scripts/code_style_checker.py .

# 检查Maya相关文件
python .codebuddy/skills/py-style/scripts/code_style_checker.py maya/tools/
```

## 检查清单

生成Maya相关代码时，确保：

- [ ] 文件头格式正确
- [ ] 包含必要的future导入
- [ ] Python 2/3兼容性处理
- [ ] 修改场景的函数使用@undoable装饰器
- [ ] 错误消息使用中文
- [ ] 使用类型注解
- [ ] 文档字符串遵循Google风格
- [ ] 异常处理完善
- [ ] 资源清理使用atexit或上下文管理器
- [ ] Maya节点操作前检查节点是否存在
- [ ] 使用assert进行参数验证

## 总结

✅ 已成功整合CurveRig工具包的代码风格
✅ 创建了完整的Maya代码风格指南
✅ 提供了丰富的Maya工具包示例代码
✅ 更新了Skill文档和说明
✅ 添加了详细的检查清单

现在Code Style Skill支持通用Python代码和Maya专用代码两种风格规范！
