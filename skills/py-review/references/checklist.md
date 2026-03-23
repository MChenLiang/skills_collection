# 代码清理检查清单

## 执行前检查

- [ ] 已运行 `preview` 命令预览将要删除的函数
- [ ] 仔细检查预览列表，确认没有误判
- [ ] 确认项目已提交到 Git（可回滚）
- [ ] 了解备份机制：`.backup_cleaner` 目录

## 常见误判提示

以下函数可能被误判，请额外注意：

### 动态调用情况
- 通过字符串调用：`getattr(module, func_name)()`
- UI 文件连接的信号处理函数
- 框架/插件系统注册的回调函数
- 魔术方法：`__init__`, `__str__`, `__getitem__` 等

### 特殊命名函数
- Qt 信号处理：`on_button_clicked`, `on_*_changed`
- Maya 插件：`initializePlugin`, `uninitializePlugin`
- 主入口：`main`, `create_ui`
- 注册函数：`register`, `unregister`

## 执行后验证

- [ ] 运行项目主要功能测试
- [ ] 检查是否有导入错误
- [ ] 验证 linter 没有新错误
- [ ] 如有问题，从 `.backup_cleaner` 恢复

## 恢复方法

```bash
# 恢复单个文件
cp <项目>/.backup_cleaner/module.py <项目>/module.py

# 恢复所有备份
cp -r <项目>/.backup_cleaner/* <项目>/
```