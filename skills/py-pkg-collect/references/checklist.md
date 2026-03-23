# 依赖包收集检查清单

## 执行前检查

- [ ] 已安装 pipreqs：`<当前Python解释器> -m pip show pipreqs`
- [ ] 目标目录存在且包含 Python 文件

## 结果验证

- [ ] 检查生成的 `requirements.txt` 内容是否合理
- [ ] 检查 `requireerror.txt` 中的库是否确实无法通过 pip 安装（如 Maya 内置库）
- [ ] 如有动态导入（`importlib`），手动补充缺失的依赖

## 部署前测试

```bash
# 在新的虚拟环境中测试
<当前Python解释器> -m venv test_env
test_env/Scripts/activate  # Windows
source test_env/bin/activate  # Linux/Mac
pip install -r requirements.txt
```

## 常见问题

**没有找到 Python 文件**：检查路径是否正确，是否被排除规则过滤

**生成的 requirements.txt 为空**：检查是否只使用了标准库，或过滤规则过于严格

**Maya 库版本号错误**：maya、pymel 等会显示 PyPI 上的错误版本，实际使用 Maya 内置版本
