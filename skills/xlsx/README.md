# Excel 操作技能

这个技能提供了完整的 Excel 和 CSV 文件处理能力。

## 功能特性

### 📊 文件操作
- 创建新的 Excel 文件
- 读取和编辑现有 Excel 文件
- CSV 文件读写
- 多工作表处理

### 🎨 格式美化
- 字体样式设置
- 单元格对齐
- 背景色和边框
- 条件格式
- 合并单元格

### 📈 数据处理
- 添加公式和函数
- 创建图表
- 数据透视表
- 数据筛选和排序
- 批量操作

### ⚙️ 高级功能
- 冻结窗格
- 自动筛选
- 数据验证
- 页眉页脚
- 打印设置

## 安装依赖

```bash
python -m pip install openpyxl pandas xlsxwriter xlrd xlwt
```

## 快速开始

### 创建简单的 Excel 文件

```python
from openpyxl import Workbook

wb = Workbook()
ws = wb.active

ws.append(["姓名", "年龄", "分数"])
ws.append(["张三", 25, 95])
ws.append(["李四", 30, 88])

wb.save("test.xlsx")
```

### 读取 Excel 文件

```python
from openpyxl import load_workbook

wb = load_workbook("test.xlsx")
ws = wb.active

for row in ws.iter_rows(values_only=True):
    print(row)
```

### 使用 Pandas 处理数据

```python
import pandas as pd

# 读取
df = pd.read_excel("test.xlsx")

# 处理
filtered = df[df['年龄'] > 25]

# 保存
filtered.to_excel("output.xlsx", index=False)
```

## 使用示例

查看 [SKILL.md](SKILL.md) 获取完整的 API 文档和使用示例。

## 技术栈

- **openpyxl** - Excel 文件读写和格式化
- **pandas** - 数据处理和分析
- **xlsxwriter** - 高性能 Excel 文件创建

## 注意事项

- openpyxl 只支持 .xlsx 格式，不支持 .xls
- 大文件操作建议使用 read_only/write_only 模式
- 处理中文时注意编码问题（推荐使用 UTF-8）

## 贡献

欢迎提交问题和改进建议！
