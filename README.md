# skills_collection

AI 辅助技能集合，提供各种开发场景下的智能辅助能力。

## 技能列表

### 📂 [git](./skills/git/)
Git 版本控制系统助手。帮助用户进行各种 Git 操作，从基础命令到高级工作流，包括初始化、提交、分支管理、冲突解决、Git Flow 等完整功能。

**核心功能**：
- 基础 Git 操作（初始化、克隆、提交、推送）
- 分支管理（创建、切换、合并、变基）
- 远程操作（fetch、pull、push）
- Git Flow 工作流支持
- 冲突解决和故障排查
- 包含 `git_helper.py` 脚本提供 Python API 和命令行接口

---

### 🐍 [py-executor](./skills/py-executor/)
Python 代码生成与执行技能。将用户的自然语言请求转化为可执行的 Python 代码并自动执行，适用于需要通过 Python 代码完成的功能性任务。

**核心功能**：
- 文件操作（批量处理、格式转换、内容提取）
- 数据操作（清洗、转换、分析、可视化）
- 网络请求（下载文件、爬取网页、API 调用）
- 系统操作（执行命令行、进程管理）
- 自动化任务和工作流

---

### 📦 [py-pkg-collect](./skills/py-pkg-collect/)
Python 依赖包收集分析技能。使用 `pkg_collect.py` 工具扫描项目代码，自动识别导入的第三方包并生成 `requirements.txt` 文件。

**核心功能**：
- 自动分析 Python 项目依赖
- 生成 requirements.txt 文件
- 识别未安装的第三方库
- 智能过滤测试文件、构建目录、临时文件
- 基于 pipreqs 工具进行依赖收集

---

### 🔍 [py-review](./skills/py-review/)
代码审核技能。帮助识别和清理代码库中未被使用的函数和死代码，支持 Maya/Rez 项目环境。

**核心功能**：
- 预览未使用的函数（不修改代码）
- 删除未使用的函数（实际修改代码）
- 自动排除测试文件、构建目录、第三方包
- Qt 信号保护，保留信号处理函数
- Maya 特殊支持，识别插件入口函数
- 修改前自动备份

---

### 🎨 [py-style](./skills/py-style/)
Python 代码风格检查与优化技能。使用自动化工具检查代码风格，并根据检查结果提供优化建议和修复方案。

**核心功能**：
- 使用 `code_style_checker.py` 自动检测代码风格问题
- 命名规范检查（snake_case、PascalCase、UPPER_CASE）
- 文档字符串检查
- 导入顺序检查
- 行长度和空行检查
- 集成 Black 和 isort 进行自动格式化

---

### 💚 [vue-style](./skills/vue-style/)
Vue 3 + TypeScript 代码风格约束技能。确保生成的 Vue 代码符合项目规范，参考实际项目案例学习并应用一致的编码风格。

**核心功能**：
- Vue 3 Composition API 支持
- TypeScript 类型安全
- Element Plus UI 组件库规范
- Axios 完整封装（拦截器、重试、分片上传）
- Vuex 状态管理规范
- 路由配置和权限控制

**参考项目**：
- Vue 后台管理系统（企业级后台管理系统架构）
- VitePress 文档站点（自定义主题和插件）

---

### 📝 [vuepress-doc-formatter](./skills/vuepress-doc-formatter/)
VuePress 文档格式化专家。专门用于统一和美化 VuePress 项目的 Markdown 文档格式，提升文档的可读性和专业性。

**核心功能**：
- Frontmatter 标准化（title、description、date、tags）
- 页面头部装饰和分隔线
- VuePress 自定义容器（tip、warning、danger、info、details）
- 表格美化和代码块优化
- 图片优化和列表格式化
- 文档结构模板

---

### 📊 [xlsx](./skills/xlsx/)
Excel 文件操作技能。提供完整的 Excel 和 CSV 文件操作能力，包括数据录入、格式美化、公式计算、图表创建等功能。

**核心功能**：
- 创建和编辑 Excel 文件（使用 openpyxl）
- 读取和写入 CSV 文件（使用 pandas）
- 格式美化（字体、颜色、边框、对齐）
- 添加公式和函数
- 创建图表和数据透视表
- 数据处理和分析

**核心工具**：
- openpyxl：读写 .xlsx 文件，支持格式化
- pandas：数据处理和分析，CSV 读写
- xlsxwriter：创建高性能 Excel 文件

---

## 使用说明

每个技能都有独立的目录和详细的使用文档。进入相应的技能目录查看 `SKILL.md` 文件以获取完整的使用说明和示例。

```bash
# 示例：使用 git 技能
cd skills/git
# 查看 SKILL.md 获取详细说明
```

## 贡献指南

欢迎贡献新的技能或改进现有技能。请确保：

1. 遵循现有的目录结构
2. 提供完整的 SKILL.md 文档
3. 包含必要的脚本和工具
4. 添加使用示例和最佳实践

## 许可证

详见 [LICENSE](./LICENSE) 文件。
