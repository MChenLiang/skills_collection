---
name: py-executor
description: 这个技能用于将用户的 AI 助手请求转化为 Python 代码并执行。当用户请求需要执行特定任务（如文件操作、数据处理、网络请求、系统命令等）时，使用此技能生成相应的 Python 脚本并执行。适用于任何需要通过 Python 代码完成的功能性任务。
---

# Python 代码生成与执行技能

## 技能概述

这个技能的目的是将用户的自然语言请求转化为可执行的 Python 代码，并自动执行以完成任务。它充当了一个桥梁，将 AI 助手的理解能力与 Python 的实际执行能力结合起来。

## 使用场景

使用此技能的场景包括但不限于：

- **文件操作**：批量处理文件、格式转换、内容提取、文件搜索等
- **数据操作**：数据清洗、转换、分析、可视化等
- **网络请求**：下载文件、爬取网页、API 调用等
- **Git 操作**：拉取代码、提交更改、分支管理等
- **系统操作**：执行命令行工具、进程管理、环境配置等
- **文本处理**：批量重命名、内容替换、日志分析等
- **自动化任务**：定时任务、批量处理、工作流自动化等

## 工作流程

### 步骤 1：理解用户需求

分析用户的请求，明确以下信息：

1. **任务类型**：确定属于哪类操作（文件、网络、数据、系统等）
2. **输入参数**：识别用户提供的参数（路径、URL、配置等）
3. **输出期望**：了解用户期望的输出形式（文件、结果、报告等）
4. **约束条件**：注意任何特殊要求（错误处理、重试机制、日志记录等）

### 步骤 2：设计 Python 代码结构

根据需求设计 Python 脚本的基本结构：

```python
#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
[任务描述] - 自动生成的脚本
创建时间: [timestamp]
"""

import sys
import os
import json
import logging
from pathlib import Path
from datetime import datetime
from typing import Any, Optional

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('execution.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


def main():
    """主函数"""
    logger.info("=== 任务开始 ===")
    logger.info(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        # 任务实现代码
        result = execute_task()
        
        logger.info("=== 任务完成 ===")
        logger.info(f"结束时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        return result
        
    except Exception as e:
        logger.error(f"任务执行失败: {e}", exc_info=True)
        return {"status": "error", "message": str(e)}


def execute_task():
    """执行具体任务"""
    # 实现具体逻辑
    pass


if __name__ == "__main__":
    result = main()
    
    # 如果返回值是字典，可以输出为 JSON 格式
    if isinstance(result, dict):
        print("\n=== 执行结果 ===")
        print(json.dumps(result, ensure_ascii=False, indent=2))
```

### 步骤 3：生成 Python 文件

1. **确定文件位置**：
   - 默认保存到临时目录
   - 使用时间戳生成唯一文件名：`task_{timestamp}.py`

2. **写入代码**：
   - 使用 `write_to_file` 工具创建 Python 文件
   - 确保包含完整的导入语句和错误处理

### 步骤 4：执行 Python 文件

使用 `execute_command` 工具执行生成的脚本：

```bash
python {script_path}
```

执行注意事项：
- 使用绝对路径
- 确保在正确的环境中执行（虚拟环境、正确的 Python 版本）
- 捕获并显示输出和错误信息

### 步骤 5：处理执行结果

1. **成功情况**：
   - 显示执行结果
   - 提供输出文件路径（如果有）
   - 总结任务完成情况

2. **失败情况**：
   - 分析错误信息
   - 提供修复建议
   - 如需要，修改代码后重新执行

## 代码生成最佳实践

### 1. 使用标准库优先

优先使用 Python 标准库，减少外部依赖：

```python
import os          # 文件和目录操作
import sys         # 系统相关
import json        # JSON 处理
import shutil      # 高级文件操作
import subprocess  # 执行系统命令
import urllib.request  # 网络请求
import re          # 正则表达式
from pathlib import Path  # 现代路径操作
```

### 2. 完善的错误处理

```python
def execute_task():
    try:
        # 任务代码
        pass
    except FileNotFoundError as e:
        logger.error(f"文件未找到: {e}")
        raise
    except PermissionError as e:
        logger.error(f"权限错误: {e}")
        raise
    except Exception as e:
        logger.error(f"未知错误: {e}")
        raise
```

### 3. 进度反馈

对于长时间运行的任务，提供进度反馈：

```python
def process_files(files):
    total = len(files)
    for i, file in enumerate(files, 1):
        logger.info(f"处理进度: {i}/{total} - {file}")
        # 处理文件
```

### 4. 清理临时文件

创建临时目录用于存放中间文件，任务完成后清理：

```python
import tempfile
import shutil

temp_dir = tempfile.mkdtemp(prefix="task_")
try:
    # 使用临时目录
    pass
finally:
    # 清理临时目录
    shutil.rmtree(temp_dir, ignore_errors=True)
```

## 常见任务模板

### 模板 1：批量文件操作

```python
import os
from pathlib import Path

def batch_rename(directory, pattern, replacement):
    """批量重命名文件"""
    for file in Path(directory).glob(pattern):
        new_name = file.name.replace(pattern, replacement)
        new_path = file.parent / new_name
        file.rename(new_path)
        logger.info(f"重命名: {file.name} -> {new_name}")
```

### 模板 2：文件下载

```python
import urllib.request
import os

def download_file(url, save_path):
    """下载文件"""
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    
    urllib.request.urlretrieve(url, save_path)
    logger.info(f"下载完成: {save_path}")
    return save_path
```

### 模板 3：执行 Git 命令

```python
import subprocess

def git_pull(repo_path):
    """执行 git pull"""
    result = subprocess.run(
        ['git', 'pull'],
        cwd=repo_path,
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        logger.info("Git pull 成功")
        return True
    else:
        logger.error(f"Git pull 失败: {result.stderr}")
        return False
```

### 模板 4：数据处理

```python
import csv
import json

def convert_csv_to_json(csv_path, json_path):
    """CSV 转 JSON"""
    data = []
    
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        data = [row for row in reader]
    
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    logger.info(f"转换完成: {len(data)} 条记录")
    return json_path
```

## 错误处理策略

### 1. 参数验证

```python
def validate_params(params):
    """验证参数"""
    if not params.get('input_path'):
        raise ValueError("缺少必要参数: input_path")
    
    if not os.path.exists(params['input_path']):
        raise FileNotFoundError(f"路径不存在: {params['input_path']}")
```

### 2. 重试机制

```python
import time
from functools import wraps

def retry(max_retries=3, delay=1):
    """重试装饰器"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise
                    logger.warning(f"重试 {attempt + 1}/{max_retries}: {e}")
                    time.sleep(delay)
        return wrapper
    return decorator
```

## 执行后清理

1. **保留生成的脚本**：
   - 保存在 `temp_scripts/` 目录
   - 供用户参考和调试

2. **日志文件**：
   - 保存为 `execution.log`
   - 记录详细的执行信息

3. **临时文件清理**：
   - 使用 `tempfile` 模块创建临时文件
   - 任务完成后自动清理

## 注意事项

1. **安全性**：
   - 避免执行不受信任的代码
   - 对用户输入进行验证和清理
   - 不使用 `eval()` 或 `exec()`

2. **兼容性**：
   - 使用跨平台路径处理（`pathlib.Path`）
   - 考虑不同操作系统的差异

3. **性能**：
   - 对于大文件操作，使用流式处理
   - 避免一次性加载所有数据到内存

4. **用户体验**：
   - 提供清晰的进度反馈
   - 输出格式化的结果
   - 友好的错误提示

## 示例对话流程

**用户**：帮我下载这个链接的文件 https://example.com/data.zip

**助手**：
1. 理解需求：下载指定 URL 的文件
2. 生成 Python 代码（文件下载模板）
3. 保存为 `temp_scripts/task_20250324_xxxxx.py`
4. 执行脚本
5. 返回结果：下载的文件路径

**用户**：批量重命名这个目录下的所有 .txt 文件，在前面加上日期前缀

**助手**：
1. 理解需求：批量文件重命名
2. 生成 Python 代码（批量重命名模板）
3. 询问确认目录路径
4. 执行脚本
5. 返回结果：重命名的文件列表

## 调试建议

如果生成的代码执行失败：

1. 检查日志文件 `execution.log`
2. 验证输入参数是否正确
3. 确认依赖是否已安装
4. 根据错误信息修改代码
5. 重新执行脚本

## 扩展建议

对于复杂任务，可以：

1. 拆分为多个子任务
2. 生成多个脚本文件
3. 创建主脚本协调执行
4. 添加配置文件支持
