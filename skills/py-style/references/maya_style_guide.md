# Maya工具包代码风格指南


## 1. 文件结构规范

### 1.1 文件头格式

所有Python文件应使用以下标准文件头：

```python
#!/usr/bin/env python
# -*- coding:UTF-8 -*-

# +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--++++ #
# 功能描述或模块说明
# +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--++++ #
```

### 1.2 导入顺序

按照以下顺序导入模块：

```python
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# 2. 分隔注释
# +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--++ #

# 3. 第三方库导入（Maya相关）
import maya.cmds as cmds
import maya.OpenMaya as om
import pymel.all as pm

# 4. 标准库导入
import os
import sys
import json
import math
import random
from functools import wraps
from concurrent.futures import ThreadPoolExecutor

# 5. 项目内部导入
from CurveRig.scripts.modules import base_commands as bcmds
from CurveRig.scripts.UI import UIName
```

## 2. Python 2/3 兼容性

### 2.1 future导入

始终使用future导入以确保兼容性：

```python
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
```

### 2.2 版本检测

使用以下模式进行版本兼容处理：

```python
import sys

_PY_3_ = sys.version_info.major > 2
if _PY_3_:
    from importlib import reload
    from subprocess import DEVNULL
else:
    DEVNULL = open(os.devnull, 'wb')

# 使用示例
if _PY_3_:
    stdout = proc.communicate()[0].strip()
else:
    stdout = proc.communicate()[0].decode().strip()
```

### 2.3 reload处理

```python
if _PY_3_:
    from importlib import reload

reload(module_name)
```

## 3. Maya特定风格

### 3.1 自定义异常

定义清晰的异常层次结构：

```python
class RigError(Exception):
    """绑定工具基础异常"""
    pass


class NodeNotFoundError(RigError):
    """节点未找到异常"""
    pass


class ValidationError(RigError):
    """验证失败异常"""
    pass
```

### 3.2 Maya装饰器

#### undoable装饰器

所有修改Maya场景的主函数都应使用undoable装饰器：

```python
from functools import wraps

def undoable(func):
    """
    添加Maya撤销记录的装饰器
    
    Args:
        func: 要包装的函数
        
    Returns:
        包装后的函数
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        cmds.undoInfo(openChunk=True)
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print("An error occurred: ", e)
            raise e
        finally:
            cmds.undoInfo(closeChunk=True)
    return wrapper

# 使用示例
@undoable
def create_joint(name: str):
    cmds.joint(name=name)
```

#### success装饰器

用于处理成功/失败状态的装饰器：

```python
def success(show_error: bool = False, show_success: bool = False):
    """
    成功/失败处理装饰器
    
    Args:
        show_error: 是否显示错误信息
        show_success: 是否显示成功信息
        
    Returns:
        装饰器函数
    """
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            try:
                result = func(self, *args, **kwargs)
            except Exception as e:
                exc_type, exc_value, exc_traceback_obj = sys.exc_info()
                msg = str(e)
                if show_error:
                    print(u"执行失败！\n%s" % msg)
                return False, msg
            else:
                if show_success and result:
                    print(u"执行成功! \n{}".format(result))
                return True, result
        
        wrapper.__doc__ = func.__doc__
        wrapper.__name__ = func.__name__
        return wrapper
    return decorator
```

### 3.3 Maya工具函数

#### 属性创建函数

```python
def attr_num(
    obj: str,
    attr: str,
    attr_type: str,
    min_val: float = None,
    max_val: float = None,
    dv: float = None,
    keyable: bool = True
) -> str:
    """
    添加数值属性
    
    Args:
        obj: 对象名称
        attr: 属性名称
        attr_type: 属性类型
        min_val: 最小值
        max_val: 最大值
        dv: 默认值
        keyable: 是否可关键帧
        
    Returns:
        str: 属性完整名称
    """
    if cmds.objExists(obj + "." + attr):
        return obj + "." + attr
    
    kwargs = {"ln": attr, "at": attr_type, "k": int(keyable)}
    
    if min_val is not None:
        kwargs["min"] = min_val
    if max_val is not None:
        kwargs["max"] = max_val
    if dv is not None:
        kwargs["dv"] = dv
    
    cmds.addAttr(str(obj), **kwargs)
    return obj + "." + attr


# 便捷函数
def attr_float(obj: str, attr: str, min_val=None, max_val=None, dv=None, k=1) -> str:
    """添加浮点属性"""
    return attr_num(obj, attr, 'double', min_val, max_val, dv, k)

def attr_int(obj: str, attr: str, min_val=None, max_val=None, dv=None, k=1) -> str:
    """添加整数属性"""
    return attr_num(obj, attr, 'long', min_val, max_val, dv, k)

def attr_bool(obj: str, attr: str, dv=0, k=1) -> str:
    """添加布尔属性"""
    return attr_num(obj, attr, 'bool', dv=dv, k=k)
```

#### 节点操作函数

```python
def get_all_parents(obj: str) -> list:
    """
    获取物体的所有父节点，从直接父级到最顶层
    
    Args:
        obj: Maya对象名称
        
    Returns:
        list: 父节点列表
        
    Raises:
        NodeNotFoundError: 如果对象不存在
    """
    if not cmds.objExists(obj):
        raise NodeNotFoundError(u"未找到对象：%s" % obj)
    
    parents = []
    current_parent = cmds.listRelatives(obj, parent=True)
    
    while current_parent:
        parents.append(current_parent[0])
        current_parent = cmds.listRelatives(parents[-1], parent=True)
    
    return parents
```

#### 命名函数

```python
def conf_naming(keyword: str, suffix: str = "") -> str:
    """
    配置命名，确保名称唯一
    
    Args:
        keyword: 关键字
        suffix: 后缀
        
    Returns:
        str: 唯一名称
        
    Raises:
        KeyError: 如果无法生成唯一名称
    """
    import string
    
    for k in string.ascii_uppercase:
        for i in range(100):
            h_word = keyword + '_%s%d' % (k, i + 1)
            if suffix:
                h_word += "_%s" % suffix
            if not cmds.objExists(h_word):
                return h_word
    
    raise KeyError('Please enter an identifying name')
```

### 3.4 类定义风格

#### 基本类结构

```python
class RigBuilder(object):
    """
    绑定构建器
    
    属性:
        keyword: 命名关键字
        root_jnt: 根关节
        curve: 曲线列表
    """
    
    # 类属性定义
    dy_top_grp = "dyn_chains_ws_grp"
    dy_out_c_grp = "dyn_chains_out_c_grp"
    dy_ik_grp = "dyn_chains_ik_grp"
    dy_ctrl_grp = "dyn_chains_ctrl_grp"
    dy_jnt_fit_grp = "dyn_chains_fit_grp"
    
    def __init__(self):
        """初始化构建器"""
        self._keyword = ""
        self._root_jnt = ""
        self._curve = []
    
    # 使用property装饰器
    @property
    def keyword(self) -> str:
        """命名关键字"""
        return self._keyword
    
    @keyword.setter
    def keyword(self, value: str):
        self._keyword = value
    
    @property
    def root_jnt(self) -> str:
        """根关节"""
        return self._root_jnt
    
    @root_jnt.setter
    def root_jnt(self, value: str):
        assert cmds.objExists(value), KeyError(u"没有找到根骨骼：%s" % value)
        self._root_jnt = value
```

#### Qt类定义

```python
from Qt.QtWidgets import QMainWindow

class MainFunc(window_class, base_class):
    def __init__(self, parent=maya_win):
        super(MainFunc, self).__init__(parent=parent)
        
        self._create_func = create.Create()
        self._verify = verify.socketHandler()
        
        self.setupUi(self)
        self._init_ui()
        self._bt_clicked()
    
    def _init_ui(self):
        """初始化UI"""
        self.widget_root_jnt.setEnabled(False)
        self.label_conf_ctrl_dis.setEnabled(False)
    
    @Slot()
    def on_button_clicked(self):
        """按钮点击事件"""
        pass
```

## 4. 命名规范

### 4.1 Maya特定命名

```python
# 关节命名
joint_name = "leg_jnt"           # 使用_jnt后缀
root_joint = "root_jnt"          # 根关节

# 控制器命名
ctrl_name = "leg_ctrl"           # 使用_ctrl后缀
sec_ctrl = "leg_cl_ctrl"         # 次级控制器使用_cl前缀

# 组命名
grp_name = "grp_leg"             # 使用grp_前缀
offset_grp = "grp_offset_leg"    # 偏移组

# 曲线命名
curve_name = "crv_leg"           # 使用_crv后前缀
```

### 4.2 私有属性

```python
class MyClass(object):
    def __init__(self):
        # 使用单个下划线表示受保护的属性
        self._keyword = ""
        self._root_jnt = ""
        self._curve = []
```

## 5. 文档字符串

### 5.1 Google风格

```python
def create_joint(
    name: str,
    position: tuple = None,
    parent: str = None
) -> str:
    """
    创建关节
    
    Args:
        name: 关节名称
        position: 世界坐标位置 (x, y, z)
        parent: 父关节名称
        
    Returns:
        str: 创建的关节名称
        
    Raises:
        NodeNotFoundError: 如果父节点不存在
        RuntimeError: 如果创建失败
        
    Examples:
        >>> create_joint("leg_jnt", (0, 10, 0))
        'leg_jnt'
    """
    if position:
        cmds.joint(name=name, position=position)
    else:
        cmds.joint(name=name)
    
    if parent:
        cmds.parent(name, parent)
    
    return name
```

## 6. 错误处理

### 6.1 使用中文错误消息

```python
# 错误消息使用中文
assert cmds.objExists(value), KeyError(u"没有找到根骨骼：%s" % value)
raise NodeNotFoundError(u"未找到对象：%s" % obj)
print(u"执行成功！\n{}".format(result))
print(u"执行失败！\n%s" % msg)

# 使用u前缀确保Unicode字符串
error_msg = u"节点不存在：%s" % node_name
```

### 6.2 异常捕获

```python
try:
    result = some_function()
except Exception as e:
    print(u"发生错误：", str(e))
    raise e
```

## 7. 注释风格

### 7.1 分隔线

使用特殊分隔线分隔代码块：

```python
# +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+ #
# 导入语句
# +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+ #

# +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+ #
# 类定义
# +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+ #
```

### 7.2 行内注释

```python
# 解锁节点
cmds.lockNode('initialParticleSE', lock=False, lockUnpublished=False)

# 获取当前选择的变换节点
type_transform = cmds.ls(selection=True)[0]

# 刷新视图
cmds.refresh()
```

## 8. 最佳实践

### 8.1 资源清理

```python
import atexit

class ResourceManager(object):
    def __init__(self):
        self._resource = None
        # 确保应用退出时清理资源
        atexit.register(self.cleanup)
    
    def cleanup(self):
        """清理资源"""
        if self._resource:
            self._resource.close()
            self._resource = None
    
    def __del__(self):
        """析构函数确保资源释放"""
        self.cleanup()
```

### 8.2 使用property验证

```python
class RigBuilder(object):
    @property
    def root_jnt(self) -> str:
        """根关节"""
        return self._root_jnt
    
    @root_jnt.setter
    def root_jnt(self, value: str):
        assert cmds.objExists(value), KeyError(u"没有找到根骨骼：%s" % value)
        self._root_jnt = value
```

### 8.3 Maya节点锁定

```python
def unlock_nodes():
    """解锁Maya默认节点"""
    cmds.lockNode('initialParticleSE', lock=False, lockUnpublished=False)
    cmds.lockNode('initialShadingGroup', lock=False, lockUnpublished=False)
    cmds.lockNode('renderPartition', lock=False, lockUnpublished=False)
    cmds.lockNode('defaultShaderList*', lock=False, lockUnpublished=False)


```

## 9. 完整示例

### 9.1 Maya工具模块模板

```python
#!/usr/bin/env python
# -*- coding:UTF-8 -*-
"""
Maya工具模块模板
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--++++ #
# 导入语句
# +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--++++ #
import maya.cmds as cmds

import sys
import os
from functools import wraps

# +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+ #
# 自定义异常
# +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+ #
class ToolError(Exception):
    """工具异常基类"""
    pass


# +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+ #
# 装饰器
# +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+ #
def undoable(func):
    """添加Maya撤销记录的装饰器"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        cmds.undoInfo(openChunk=True)
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print("An error occurred: ", e)
            raise e
        finally:
            cmds.undoInfo(closeChunk=True)
    return wrapper


# +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+ #
# 主类
# +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+ #
class MayaTool(object):
    """Maya工具基类"""
    
    def __init__(self):
        """初始化"""
        pass
    
    @undoable
    def do_something(self):
        """执行某个操作"""
        pass


if __name__ == "__main__":
    main()
```

## 10. 检查清单

生成Maya相关代码时，请检查以下项目：

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
