---
name: py-pkg-collect
description: 当用户请求分析 Python 项目依赖、生成 requirements.txt 或了解项目使用的第三方库时使用此技能。使用 pkg_collect.py 工具扫描项目代码，自动识别导入的第三方包并生成依赖列表。
---

# Python 依赖包收集分析技能

此技能提供 Python 依赖分析的专业能力，专注于识别项目中的第三方库并生成 requirements.txt 文件。

## 何时使用此技能

- 用户需要分析 Python 项目的依赖
- 用户需要生成 requirements.txt 文件
- 用户需要了解项目使用了哪些第三方库
- 用户需要将项目迁移到新环境
- 用户需要为项目打包或部署做准备

## 核心工具

使用 `pkg_collect.py` 脚本执行依赖分析：
- **脚本路径**：`.codebuddy/skills/py-pkg-collect/scripts/pkg_collect.py`
- **执行方式**：使用当前 Python 解释器执行
- **底层工具**：基于 pipreqs 进行依赖收集

## 使用方法

### 基本命令

```bash
<当前Python解释器> .codebuddy/skills/py-pkg-collect/scripts/pkg_collect.py analysis <目标目录>
```

### 前置条件

确保已安装依赖：
```bash
<当前Python解释器> -m pip install pipreqs fire
```

## 输出文件

分析完成后生成两个文件：

1. **requirements.txt** - 已安装的第三方库及版本号
   ```
   numpy==1.21.0
   pandas==1.3.0
   ```

2. **requireerror.txt** - 代码中使用但 pipreqs 无法检测版本的库
   ```
   # 未安装的第三方库
   Qt
   ```

## 内置功能

脚本已自动处理：

- **过滤规则**：排除测试文件、构建目录、临时文件等
- **标准库过滤**：自动排除 Python 标准库
- **临时目录**：使用临时目录进行分析，自动清理

## 注意事项

- 动态导入（`importlib`、`__import__`）可能无法识别
- 未安装的库会写入 `requireerror.txt`
- Maya 特殊库（maya、pymel）可能被误判版本号
- 建议在干净的虚拟环境中运行
