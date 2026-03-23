# Vue 代码风格 Skill - Vue 3 + TypeScript 代码风格约束

## 概述

这是一个用于约束和检查 Vue 3 + TypeScript 代码风格的 Skill，支持 **3 种代码风格规范**，确保生成的代码符合不同场景的编码规范。

## 支持的代码风格

### 1. Vue 后台管理系统风格 ⭐ 推荐
**适用场景**：企业级后台管理系统、CRUD 应用、数据展示
**参考来源**：`E:\working\website\NCHome\backend`

**主要特点**：
- ✅ TypeScript + Vue 3 Composition API
- ✅ `<script setup lang="ts">` 语法
- ✅ Vuex 状态管理
- ✅ Element Plus UI 组件库
- ✅ Axios 完整封装（拦截器、重试、分片上传）
- ✅ 动态路由权限控制

### 2. VitePress 文档站点风格
**适用场景**：文档站点、博客、静态页面
**参考来源**：`E:\working\website\NCHome\docs`

**主要特点**：
- ✅ VuePress 2.x 自定义主题
- ✅ 自定义插件开发
- ✅ SSR 兼容性处理
- ✅ MutationObserver 监听主题变化
- ✅ 动态侧边栏生成

### 3. 通用 Vue 3 风格
**适用场景**：通用 Vue 3 应用、工具组件
**参考来源**：Vue 3 官方文档和最佳实践

**主要特点**：
- ✅ Vue 3 Composition API
- ✅ TypeScript 类型安全
- ✅ Props/Emits 类型定义
- ✅ 组件通信模式

## 目录结构

```
vue-style/
├── SKILL.md                        (25 KB)   - Skill 主文档（3种风格规范）
├── README.md                       (本文件)   - 完整说明文档
├── QUICKSTART.md                   - 快速开始指南
└── references/
    └── examples/                    # 代码示例
        ├── vue_admin_component.vue # Vue 后台组件示例 ⭐
        ├── vitepress_page.vue      # VitePress 页面示例
        └── axios_instance.ts      # Axios 封装示例
```

## 功能特性

### 1. Vue 后台管理系统风格

#### 技术栈
| 技术 | 用途 |
|-----|------|
| Vue 3 | 前端框架 |
| TypeScript | 类型安全 |
| Vite | 构建工具 |
| Vue Router 4 | 路由管理（Hash 模式）|
| Vuex 4 | 状态管理 |
| Element Plus | UI 组件库 |
| Axios | HTTP 请求 |
| Day.js | 日期处理 |

#### 代码规范
- ✅ **文件命名**：小驼峰（`FormData.vue`）
- ✅ **组件命名**：大驼峰（`MyComponent`）
- ✅ **变量命名**：小驼峰（`user_data`）
- ✅ **常量命名**：全大写下划线（`API_URL`）
- ✅ **函数命名**：小驼峰动词开头（`handle_add`）
- ✅ **Props 命名**：前缀 `init_`（`init_page_title`）

#### 核心特性
- **Axios 封装**：
  - 请求拦截器：自动添加 Bearer Token
  - 响应拦截器：处理 401 错误（自动跳转登录）
  - 重试机制：指数退避策略，默认重试 3 次
  - 超时配置：默认 5000ms

- **组件设计**：
  - 使用 `<script setup>` 语法
  - Composition API
  - TypeScript 接口定义
  - Scoped 样式

- **路由配置**：
  - Hash 模式
  - 路由守卫
  - 动态导入

- **状态管理**：
  - Vuex Store
  - 模块化状态
  - Getters/Mutations/Actions

### 2. VitePress 文档站点风格

#### 技术栈
| 技术 | 用途 |
|-----|------|
| VuePress 2.x | 静态站点生成器 |
| Vite | 构建工具 |
| Vue 3 | 前端框架 |
| TypeScript | 类型安全 |
| @vuepress/theme-default | 默认主题 |
| Element Plus | UI 组件库 |
| Vuex | 状态管理 |

#### 代码规范
- ✅ **文件命名**：小驼峰（`NCHome.vue`）
- ✅ **组件命名**：NC 前缀（`NCLogin`）
- ✅ **函数命名**：小驼峰（`readDirectory`）

#### 核心特性
- **自定义主题**：
  - 覆盖默认主题布局
  - 自定义组件
  - 全局样式

- **自定义插件**：
  - 文件系统操作
  - 树形结构处理
  - Frontmatter 扩展

- **SSR 兼容**：
  - 服务端渲染支持
  - 客户端增强
  - MutationObserver 使用

### 3. 通用 Vue 3 风格

#### Composition API
- ✅ `ref` 和 `reactive` 响应式数据
- ✅ `computed` 计算属性
- ✅ `watch` 和 `watchEffect` 监听器
- ✅ 生命周期钩子（`onMounted`、`onBeforeUnmount`）
- ✅ `provide` 和 `inject` 依赖注入

#### TypeScript
- ✅ 接口定义
- ✅ 类型推断
- ✅ 泛型使用
- ✅ 类型断言

#### 组件通信
- ✅ Props 和 Emits 类型定义
- ✅ 插槽使用（作用域插槽）
- ✅ `defineExpose` 暴露方法
- ✅ `defineModel` 双向绑定

## 参考案例

### 优秀案例（examples/）

1. **vue_admin_component.vue** - Vue 后台组件 ⭐ **推荐**
   - 完整的 CRUD 页面示例
   - Element Plus 表格、分页、对话框
   - 搜索、编辑、删除功能
   - TypeScript 类型定义
   - Composition API 使用

2. **vitepress_page.vue** - VitePress 页面
   - 自定义首页组件
   - 主题切换逻辑
   - MutationObserver 使用示例
   - 响应式设计
   - 暗色模式支持

3. **axios_instance.ts** - Axios 封装
   - 完整的 Axios 配置
   - 认证拦截器
   - 重试拦截器（指数退避）
   - TypeScript 接口定义
   - 错误处理

## 快速开始

### 1. 查阅文档

```bash
# 查看完整的代码风格规范
cat .codebuddy/skills/vue-style/SKILL.md

# 查看快速开始指南
cat .codebuddy/skills/vue-style/QUICKSTART.md
```

### 2. 学习示例

```bash
# Vue 后台组件示例
cat .codebuddy/skills/vue-style/references/examples/vue_admin_component.vue

# VitePress 页面示例
cat .codebuddy/skills/vue-style/references/examples/vitepress_page.vue

# Axios 封装示例
cat .codebuddy/skills/vue-style/references/examples/axios_instance.ts
```

### 3. 生成代码

告诉系统你需要生成什么类型的组件或页面，系统会自动应用相应的代码风格规范。

**示例**：
```
"生成一个用户管理页面，使用 Element Plus，包含增删改查功能"
"生成一个 VitePress 首页组件，支持主题切换"
"封装一个 API 请求模块，使用 TypeScript"
```

## 代码风格检查清单

### 命名规范
- [ ] 文件名使用小驼峰（`FormData.vue`）
- [ ] 组件名使用大驼峰（`MyComponent`）
- [ ] 变量名使用小驼峰（`user_data`）
- [ ] 常量名使用全大写下划线（`API_URL`）
- [ ] Props 使用前缀 `init_`（`init_page_title`）

### 组件结构
- [ ] 使用 `<script setup lang="ts">` 语法
- [ ] Props 使用 TypeScript 类型定义
- [ ] Emits 使用类型定义
- [ ] 使用 `computed` 替代 `methods` 中的计算逻辑
- [ ] 合理使用 `watch` 监听数据变化

### API 请求
- [ ] 使用封装的 Axios 实例
- [ ] 定义 TypeScript 接口
- [ ] 使用 async/await 处理异步
- [ ] 添加错误处理

### 样式
- [ ] 使用 `scoped` 避免样式污染
- [ ] 深度选择器使用 `:deep()` 或 `::v-deep()`
- [ ] 语义化类名

### TypeScript
- [ ] 定义清晰的接口类型
- [ ] 使用类型断言时添加注释
- [ ] 避免使用 `any` 类型

## 参考资源

- [Vue 3 官方文档](https://vuejs.org/)
- [TypeScript 官方文档](https://www.typescriptlang.org/)
- [Vite 官方文档](https://vitejs.dev/)
- [VuePress 官方文档](https://vuepress.vuejs.org/)
- [Element Plus 官方文档](https://element-plus.org/)
- [Pinia 官方文档](https://pinia.vuejs.org/)
- [Vue Router 官方文档](https://router.vuejs.org/)

## 项目示例

### Vue 后台管理系统
- **源码位置**：`E:\working\website\NCHome\backend`
- **技术栈**：Vue 3 + TypeScript + Vite + Element Plus + Vuex
- **架构特点**：企业级后台管理系统，完整的权限控制、数据管理、文件上传

### VitePress 文档站点
- **源码位置**：`E:\working\website\NCHome\docs`
- **技术栈**：VuePress 2 + TypeScript + Vite
- **架构特点**：文档站点 + 业务页面混合，自定义主题和插件

## 总结

✅ 已成功整合 Vue 后台管理系统和 VitePress 文档站点的代码风格
✅ 创建了完整的 Vue 3 + TypeScript 代码风格规范
✅ 提供了丰富的示例代码
✅ 支持多种应用场景（后台管理、文档站点、通用应用）
✅ 添加了详细的检查清单

现在 Vue Style Skill 支持后台管理系统、文档站点和通用应用三种风格规范！
