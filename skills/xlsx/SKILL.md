---
name: xlsx
description: 当用户需要创建、编辑、读取、处理 Excel 或 CSV 文件时使用此技能。提供完整的 Excel 文件操作能力，包括数据录入、格式美化、公式计算、图表创建等功能。
---

# Excel 文件操作技能

此技能提供专业的 Excel 和 CSV 文件处理能力，帮助用户高效处理电子表格数据。

## 何时使用此技能

- 用户需要创建新的 Excel 文件
- 用户需要编辑或修改现有 Excel 文件
- 用户需要读取 Excel 文件内容
- 用户需要美化 Excel 文件格式
- 用户需要添加公式和函数
- 用户需要创建图表和数据透视表
- 用户需要处理 CSV 文件
- 用户需要进行数据分析和整理

## 核心工具

使用 Python 的 `openpyxl`、`pandas` 和 `xlsxwriter` 库进行 Excel 操作：

- **openpyxl**：读写 .xlsx 文件，支持格式化
- **pandas**：数据处理和分析，CSV 读写
- **xlsxwriter**：创建高性能 Excel 文件

## 前置条件

确保已安装必要依赖：
```bash
python -m pip install openpyxl pandas xlsxwriter xlrd xlwt
```

## 常用操作

### 1. 创建新的 Excel 文件

```python
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side

# 创建工作簿
wb = Workbook()
ws = wb.active
ws.title = "工作表1"

# 添加数据
ws['A1'] = "姓名"
ws['B1'] = "年龄"
ws['C1'] = "分数"

ws.append(["张三", 25, 95])
ws.append(["李四", 30, 88])

# 保存文件
wb.save("output.xlsx")
```

### 2. 读取 Excel 文件

```python
from openpyxl import load_workbook

# 加载工作簿
wb = load_workbook("input.xlsx")

# 获取工作表
ws = wb.active
# 或指定工作表名
ws = wb["工作表1"]

# 读取数据
for row in ws.iter_rows(values_only=True):
    print(row)

# 读取特定单元格
value = ws['A1'].value
```

### 3. 使用 Pandas 读写 Excel

```python
import pandas as pd

# 读取 Excel
df = pd.read_excel("input.xlsx", sheet_name="Sheet1")

# 写入 Excel
df.to_excel("output.xlsx", index=False, engine='openpyxl')

# 读取多个工作表
excel_file = pd.ExcelFile("input.xlsx")
sheet_names = excel_file.sheet_names
```

### 4. 格式美化

```python
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.utils import get_column_letter

# 设置字体
font = Font(name='微软雅黑', size=12, bold=True, color='FF0000')
ws['A1'].font = font

# 设置对齐方式
alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
ws['A1'].alignment = alignment

# 设置背景色
fill = PatternFill(start_color='4472C4', end_color='4472C4', fill_type='solid')
ws['A1'].fill = fill

# 设置边框
thin_border = Border(
    left=Side(style='thin'),
    right=Side(style='thin'),
    top=Side(style='thin'),
    bottom=Side(style='thin')
)
ws['A1'].border = thin_border

# 自动调整列宽
for column in ws.columns:
    max_length = 0
    column_letter = get_column_letter(column[0].column)
    for cell in column:
        try:
            if len(str(cell.value)) > max_length:
                max_length = len(str(cell.value))
        except:
            pass
    adjusted_width = (max_length + 2)
    ws.column_dimensions[column_letter].width = adjusted_width
```

### 5. 添加公式

```python
# 添加公式
ws['D2'] = "=SUM(B2:C2)"
ws['E2'] = "=AVERAGE(B2:D2)"
ws['F2'] = "=IF(D2>60,\"及格\",\"不及格\")"
```

### 6. 条件格式

```python
from openpyxl.formatting.rule import CellIsRule
from openpyxl.styles import PatternFill

# 添加条件格式
red_fill = PatternFill(start_color='FF0000', end_color='FF0000', fill_type='solid')
ws.conditional_formatting.add(
    'C2:C100',
    CellIsRule(operator='lessThan', formula=['60'], fill=red_fill)
)
```

### 7. 创建图表

```python
from openpyxl.chart import BarChart, Reference

# 创建柱状图
chart = BarChart()
chart.type = "col"
chart.style = 10
chart.title = "销售数据统计"
chart.y_axis.title = '销售额'
chart.x_axis.title = '月份'

# 添加数据
data = Reference(ws, min_col=2, min_row=1, max_row=10, max_col=5)
cats = Reference(ws, min_col=1, min_row=2, max_row=10)
chart.add_data(data, titles_from_data=True)
chart.set_categories(cats)

# 添加图表到工作表
ws.add_chart(chart, "E2")
```

### 8. 冻结窗格

```python
# 冻结首行
ws.freeze_panes = 'A2'

# 冻结首列
ws.freeze_panes = 'B1'

# 冻结首行首列
ws.freeze_panes = 'B2'
```

### 9. 数据筛选

```python
# 启用自动筛选
ws.auto_filter.ref = "A1:F100"

# 设置筛选条件
ws.auto_filter.add_filter_column(0, ['张三', '李四'])
```

### 10. 批量操作

```python
# 批量设置格式
header_font = Font(bold=True, color='FFFFFF')
header_fill = PatternFill(start_color='4472C4', end_color='4472C4', fill_type='solid')
header_alignment = Alignment(horizontal='center', vertical='center')

for cell in ws[1]:
    cell.font = header_font
    cell.fill = header_fill
    cell.alignment = header_alignment

# 批量添加数据
data = [
    ["姓名", "年龄", "分数"],
    ["张三", 25, 95],
    ["李四", 30, 88],
    ["王五", 28, 92]
]

for row in data:
    ws.append(row)
```

## CSV 文件操作

### 读取 CSV

```python
import pandas as pd

# 读取 CSV
df = pd.read_csv("input.csv", encoding='utf-8')

# 指定分隔符
df = pd.read_csv("input.csv", sep=';')

# 指定编码
df = pd.read_csv("input.csv", encoding='gbk')
```

### 写入 CSV

```python
# 写入 CSV
df.to_csv("output.csv", index=False, encoding='utf-8')

# 指定分隔符
df.to_csv("output.csv", sep='\t', index=False)
```

## 数据处理示例

### 按分类分组

```python
import pandas as pd

# 读取数据
df = pd.read_excel("报价表.xlsx")

# 按大类分组
grouped = df.groupby('大类')

# 对每个分组处理
for name, group in grouped:
    print(f"分类: {name}")
    print(group)
```

### 数据透视表

```python
# 创建数据透视表
pivot = pd.pivot_table(
    df,
    values='价格',
    index='类别',
    columns='项目',
    aggfunc='sum'
)
```

### 数据筛选

```python
# 筛选数据
filtered = df[df['价格'] > 1000]
filtered = df[df['类别'] == '角色制作']
filtered = df[df['项目'].str.contains('角色')]
```

## 常用函数和公式

### Excel 公式参考

```
=SUM(A1:A10)          求和
=AVERAGE(A1:A10)      平均值
=MAX(A1:A10)          最大值
=MIN(A1:A10)          最小值
=COUNT(A1:A10)        计数
=COUNTA(A1:A10)       非空计数
=IF(A1>60,"及格","不及格")  条件判断
=VLOOKUP(A1,B:D,2,FALSE)  垂直查找
=INDEX(A:C,MATCH(查找值,A:A,0))  索引匹配
=CONCATENATE(A1,B1)   文本连接
=LEFT(A1,3)           左侧字符
=RIGHT(A1,3)          右侧字符
=MID(A1,2,3)          中间字符
=UPPER(A1)            大写
=LOWER(A1)            小写
=TODAY()              今天日期
=NOW()                当前时间
=YEAR(A1)             年份
=MONTH(A1)            月份
=DAY(A1)              日期
```

## 样式配置

### 预设配色方案

```python
# 标题样式
title_style = {
    'font': Font(name='微软雅黑', size=16, bold=True, color='FFFFFF'),
    'fill': PatternFill(start_color='4472C4', end_color='4472C4', fill_type='solid'),
    'alignment': Alignment(horizontal='center', vertical='center')
}

# 表头样式
header_style = {
    'font': Font(name='微软雅黑', size=11, bold=True, color='FFFFFF'),
    'fill': PatternFill(start_color='5B9BD5', end_color='5B9BD5', fill_type='solid'),
    'alignment': Alignment(horizontal='center', vertical='center'),
    'border': thin_border
}

# 数据样式
data_style = {
    'font': Font(name='微软雅黑', size=10),
    'alignment': Alignment(horizontal='left', vertical='center'),
    'border': thin_border
}

# 货币样式
currency_style = {
    'number_format': '"¥"#,##0.00',
    'font': Font(name='微软雅黑', size=10),
    'alignment': Alignment(horizontal='right', vertical='center')
}
```

## 常见问题

### Q1: 如何处理中文乱码？

```python
# 读取时指定编码
df = pd.read_excel("input.xlsx", encoding='utf-8')

# 写出时指定编码
df.to_csv("output.csv", encoding='utf-8-sig')
```

### Q2: 如何合并单元格？

```python
# 合并单元格
ws.merge_cells('A1:C1')
ws['A1'] = "标题"
ws['A1'].alignment = Alignment(horizontal='center', vertical='center')
```

### Q3: 如何删除行或列？

```python
# 删除行
ws.delete_rows(2, 3)  # 从第2行开始删除3行

# 删除列
ws.delete_cols(2, 1)  # 删除第2列
```

### Q4: 如何设置打印区域？

```python
# 设置打印区域
ws.print_area = "A1:F100"

# 设置打印标题
ws.print_title_rows = "1:1"
ws.print_title_cols = "A:A"
```

### Q5: 如何添加页眉页脚？

```python
# 添加页眉
ws.header_footer.differentFirst = True
ws.header_footer.firstHeader.center = "第一页页眉"
ws.header_footer.oddHeader.center = "页眉内容"

# 添加页脚
ws.header_footer.oddFooter.center = "第 &P 页，共 &N 页"
```

## 性能优化

### 大文件处理

```python
# 使用只读模式
wb = load_workbook(filename='large.xlsx', read_only=True)

# 使用写优化模式
wb = Workbook(write_only=True)
ws = wb.create_sheet()

# 批量写入数据
for row in large_data:
    ws.append(row)

wb.save('output.xlsx')
```

## 示例脚本

### 完整示例：创建报价表

```python
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.utils import get_column_letter

# 创建工作簿
wb = Workbook()
ws = wb.active
ws.title = "报价表"

# 定义样式
title_font = Font(name='微软雅黑', size=14, bold=True, color='FFFFFF')
title_fill = PatternFill(start_color='4472C4', end_color='4472C4', fill_type='solid')
title_align = Alignment(horizontal='center', vertical='center')

header_font = Font(name='微软雅黑', size=11, bold=True, color='FFFFFF')
header_fill = PatternFill(start_color='5B9BD5', end_color='5B9BD5', fill_type='solid')

thin_border = Border(
    left=Side(style='thin', color='D0D0D0'),
    right=Side(style='thin', color='D0D0D0'),
    top=Side(style='thin', color='D0D0D0'),
    bottom=Side(style='thin', color='D0D0D0')
)

# 添加标题
ws.merge_cells('A1:H1')
ws['A1'] = '三维制作报价表'
ws['A1'].font = Font(name='微软雅黑', size=18, bold=True, color='4472C4')
ws['A1'].alignment = title_align

# 添加表头
headers = ['大类', '细分类型', '工作环节', '具体内容', '精度/等级', '价格区间(元)', '计量单位', '价格说明']
for col, header in enumerate(headers, start=1):
    cell = ws.cell(row=3, column=col)
    cell.value = header
    cell.font = header_font
    cell.fill = header_fill
    cell.alignment = Alignment(horizontal='center', vertical='center')
    cell.border = thin_border

# 添加数据
data = [
    ['角色制作', '次世代角色', '建模', '角色基础模型制作', '低模', '2,000-3,000', '个', '基础拓扑结构'],
    ['角色制作', '次世代角色', '建模', '角色基础模型制作', '中模', '3,000-5,000', '个', '中等细节'],
    # ... 更多数据
]

for row_idx, row_data in enumerate(data, start=4):
    for col_idx, value in enumerate(row_data, start=1):
        cell = ws.cell(row=row_idx, column=col_idx)
        cell.value = value
        cell.font = Font(name='微软雅黑', size=10)
        cell.alignment = Alignment(horizontal='left', vertical='center')
        cell.border = thin_border

# 自动调整列宽
for column in ws.columns:
    max_length = 0
    column_letter = get_column_letter(column[0].column)
    for cell in column:
        try:
            if len(str(cell.value)) > max_length:
                max_length = len(str(cell.value))
        except:
            pass
    adjusted_width = (max_length + 2) * 1.2
    ws.column_dimensions[column_letter].width = adjusted_width

# 冻结窗格
ws.freeze_panes = 'A4'

# 启用自动筛选
ws.auto_filter.ref = f"A3:H{len(data)+3}"

# 保存文件
wb.save('报价表.xlsx')
print("Excel 文件创建成功！")
```

## 最佳实践

1. **文件编码**：始终使用 UTF-8 编码处理中文
2. **数据验证**：添加数据验证确保数据质量
3. **格式统一**：使用一致的样式和格式
4. **性能考虑**：大文件使用 read_only/write_only 模式
5. **错误处理**：添加异常处理避免程序崩溃
6. **文档注释**：为关键代码添加注释说明
7. **备份文件**：操作前先备份原始文件

## 注意事项

- openpyxl 不支持 .xls 格式，只支持 .xlsx
- 大文件操作时注意内存使用
- 公式计算依赖 Excel，打开文件时才会计算
- 条件格式和图表需要保存后在 Excel 中查看
- 删除操作不可逆，建议先备份
