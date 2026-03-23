# Vue 代码风格 Skill 快速开始

## 📁 目录结构

```
vue-style/
├── SKILL.md                        (25 KB)   - Skill 主文档
├── README.md                       (本文件)   - 完整说明文档
├── QUICKSTART.md                   (本文件)   - 快速开始指南
└── references/
    └── examples/                  # 代码示例
        ├── vue_admin_component.vue  # Vue 后台组件示例
        ├── vitepress_page.vue       # VitePress 页面示例
        └── axios_instance.ts      # Axios 封装示例
```

## 🚀 立即开始使用

### 1. 查阅 Skill 文档

```bash
cat .codebuddy/skills/vue-style/SKILL.md
```

### 2. 学习优秀案例

```bash
# Vue 后台组件示例
cat .codebuddy/skills/vue-style/references/examples/vue_admin_component.vue

# VitePress 页面示例
cat .codebuddy/skills/vue-style/references/examples/vitepress_page.vue

# Axios 封装示例
cat .codebuddy/skills/vue-style/references/examples/axios_instance.ts
```

## 📚 主要内容

### SKILL.md (25 KB)

完整的代码风格规范，包含 3 种风格：

#### 1. Vue 后台管理系统风格 ⭐ **推荐**
**适用场景**：企业级后台管理系统、CRUD 应用、数据展示
**参考来源**：`E:\working\website\NCHome\backend`

**主要特点**：
- ✅ TypeScript + Vue 3 Composition API
- ✅ `<script setup lang="ts">` 语法
- ✅ Vuex 状态管理
- ✅ Element Plus UI 组件库
- ✅ Axios 封装（拦截器、重试、分片上传）
- ✅ 动态路由权限控制
- ✅ 完整的类型定义

**包含内容**：
- 项目结构规范
- 命名规范（文件名、组件名、变量名、常量名、函数名）
- 组件模板（Props、Emits、生命周期）
- Axios 封装（基础配置、拦截器、重试机制）
- API 请求封装（接口定义、类型定义）
- Vuex 状态管理（State、Getters、Mutations、Actions）
- 路由配置（路由守卫、动态路由）
- Vite 配置（路径别名、环境变量、代理）
- Element Plus 使用规范
- TypeScript 类型定义

#### 2. VitePress 文档站点风格
**适用场景**：文档站点、博客、静态页面
**参考来源**：`E:\working\website\NCHome\docs`

**主要特点**：
- ✅ VuePress 2.x 自定义主题
- ✅ 自定义插件开发
- ✅ SSR 兼容性处理
- ✅ MutationObserver 监听主题变化
- ✅ 动态侧边栏生成

**包含内容**：
- 项目结构规范
- 配置文件示例
- 自定义插件开发（Plugin API）
- 自定义主题组件
- 客户端增强

#### 3. 通用 Vue 3 风格
**适用场景**：通用 Vue 3 应用、工具组件
**参考来源**：Vue 3 官方文档

**主要特点**：
- ✅ Vue 3 Composition API
- ✅ TypeScript 类型安全
- ✅ Props/Emits 类型定义
- ✅ 组件通信模式

**包含内容**：
- Composition API 使用（ref、reactive、computed、watch）
- Props 和 Emits 类型定义
- 组件通信（父子通信、插槽、暴露方法）
- 样式规范（scoped、深度选择器）

## 🎯 使用场景

### 场景 1：生成后台管理系统组件

系统会自动应用 Vue 后台管理系统风格规范：

```vue
<template>
    <div class="page-container">
        <h1 class="page-title">{{ page_title }}</h1>

        <el-table :data="table_data" border>
            <el-table-column prop="name" label="名称" />
            <el-table-column label="操作">
                <template #default="scope">
                    <el-button @click="handle_edit(scope.row)">编辑</el-button>
                    <el-button @click="handle_delete(scope.row)" type="danger">删除</el-button>
                </template>
            </el-table-column>
        </el-table>

        <el-pagination
            v-model:current-page="current_page"
            :page-size="page_size"
            :total="total"
            @current-change="handle_page_change"
        />
    </div>
</template>

<script lang="ts" setup>
import {ref, onMounted} from "vue";
import type {Column, Product} from "~/composables/dbModInfo";

const props = defineProps({
    init_page_title: {type: String, default: "默认标题"},
    init_columns: {type: Array, default: () => []},
});

const page_title = ref(props.init_page_title);
const table_data = ref<Product[]>([]);
const current_page = ref(1);
const page_size = ref(10);
const total = ref(0);

const fetch_data = async () => {
    // API 请求
};

onMounted(() => {
    fetch_data();
});
</script>
```

### 场景 2：生成 VitePress 页面

系统会自动应用 VitePress 文档站点风格规范：

```vue
<template>
    <div class="custom-page">
        <div class="vp-hero">
            <img class="vp-hero-image" :src="logo_icon">
            <h1>{{ site_title }}</h1>
            <p class="vp-hero-description">{{ site_description }}</p>
        </div>
    </div>
</template>

<script setup lang="ts">
import {ref, onMounted, onBeforeUnmount} from "vue";

const logo_icon = ref("/images/logo.svg");

const updateLogoIcon = () => {
    const dataTheme = document.documentElement.getAttribute('data-theme');
    logo_icon.value = dataTheme === "light" ? "/images/logo.svg" : "/images/logo_dark.svg";
};

let observer: MutationObserver;

onMounted(() => {
    updateLogoIcon();
    observer = new MutationObserver(updateLogoIcon);
    observer.observe(document.documentElement, {
        attributes: true,
        attributeFilter: ['data-theme']
    });
});

onBeforeUnmount(() => {
    if (observer) observer.disconnect();
});
</script>
```

### 场景 3：封装 API 请求

```typescript
import axiosInstance from "~/composables/axiosInstance";

export interface ASSET_INFO {
    id?: number;
    name: string;
    version: string;
    description: string;
}

export async function get_asset_list(page: number = 1, page_size: number = 10) {
    const response = await axiosInstance.get(`/api/assets?page=${page}&page_size=${page_size}`);
    return response.data;
}

export async function create_asset(asset: ASSET_INFO) {
    const response = await axiosInstance.post("/api/assets", asset);
    return response.data;
}
```

## 📋 检查清单

在生成或审查代码时，确保：

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

## 🔧 集成到项目

### 1. 安装依赖

```bash
npm install vue@^3.4.0 typescript vite @vitejs/plugin-vue
npm install element-plus @element-plus/icons-vue
npm install axios vuex vue-router
npm install dayjs
```

### 2. 配置 Vite

```typescript
import {defineConfig} from 'vite';
import vue from '@vitejs/plugin-vue';
import {resolve} from 'path';

export default defineConfig({
    plugins: [vue()],
    resolve: {
        alias: {
            "~": resolve(__dirname, 'src'),
        },
    },
});
```

### 3. 配置 TypeScript

```json
{
    "compilerOptions": {
        "target": "ES2020",
        "module": "ESNext",
        "strict": true,
        "jsx": "preserve",
        "moduleResolution": "node",
        "skipLibCheck": true,
        "esModuleInterop": true,
        "allowSyntheticDefaultImports": true,
        "forceConsistentCasingInFileNames": true,
        "useDefineForClassFields": true,
        "sourceMap": true,
        "baseUrl": ".",
        "paths": {
            "~/*": ["src/*"]
        }
    },
    "include": ["src/**/*.ts", "src/**/*.d.ts", "src/**/*.tsx", "src/**/*.vue"],
    "references": [{ "path": "./tsconfig.node.json" }]
}
```

## 📖 参考资源

- [Vue 3 官方文档](https://vuejs.org/)
- [TypeScript 官方文档](https://www.typescriptlang.org/)
- [Vite 官方文档](https://vitejs.dev/)
- [VuePress 官方文档](https://vuepress.vuejs.org/)
- [Element Plus 官方文档](https://element-plus.org/)
- [Pinia 官方文档](https://pinia.vuejs.org/)
- [Vue Router 官方文档](https://router.vuejs.org/)

## 🎉 开始使用

现在你可以：

1. **生成组件**：系统会自动应用代码风格规范
2. **学习案例**：参考 `references/examples/` 中的优秀代码
3. **类型安全**：使用 TypeScript 确保代码质量
4. **最佳实践**：遵循 Composition API 和组件设计模式

**让 Vue 代码更加优雅和一致！** ✨
