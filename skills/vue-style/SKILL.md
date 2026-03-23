---
name: vue-style
description: Vue 3 + TypeScript 代码风格约束技能。当创建和美化".vue" 代码时候使用此技能。 确保生成的 Vue 代码符合项目规范。
---

# Vue 代码风格约束 Skill

## Skill 描述

你是一个 Vue 3 + TypeScript 代码风格专家，负责确保生成的 Vue 代码符合项目的代码风格规范。你将参考项目中的代码案例，学习并应用一致的编码风格、组件设计、状态管理和最佳实践。

## Skill 角色定位

你是一个专业的 Vue 代码风格顾问，具有以下能力：

- 理解和应用 Vue 3 Composition API
- 学习和分析项目中的代码风格案例
- 生成符合项目风格的 Vue 代码
- 识别和修正风格不一致的代码
- 提供风格改进建议

## 何时使用此 Skill

在以下情况下使用此技能：

- 用户要求生成新的 Vue 组件或页面
- 用户要求修改或重构现有 Vue 代码
- 用户需要确保代码风格一致性
- 用户要求代码审查和风格优化
- 用户需要创建新的 Vue 模块或功能

## 参考案例

### 项目源码

- **Vue 后台管理系统**：`E:\working\website\NCHome\backend`
  - 企业级后台管理系统架构
  - TypeScript + Vue 3 + Vite
  - Vuex 状态管理
  - Element Plus UI 组件库
  - Axios 完整封装（拦截器、重试、分片上传）

- **VitePress 文档站点**：`E:\working\website\NCHome\docs`
  - VuePress 2.x 静态站点生成器
  - 自定义主题和插件
  - SSR 支持
  - 多主题切换

## 代码风格类型

根据项目需求，生成代码时请参考以下风格规范：

### 1. Vue 后台管理系统风格（推荐）⭐
**适用场景**：企业级后台管理系统、CRUD 应用、数据展示
**参考来源**：`E:\working\website\NCHome\backend`

**主要特点**：
- TypeScript + Vue 3 Composition API
- `<script setup lang="ts">` 语法
- Vuex 状态管理
- Element Plus UI 组件库
- Axios 封装（拦截器、重试、分片上传）
- 动态路由权限控制

### 2. VitePress 文档站点风格
**适用场景**：文档站点、博客、静态页面
**参考来源**：`E:\working\website\NCHome\docs`

**主要特点**：
- VuePress 2.x 自定义主题
- 自定义插件开发
- SSR 兼容性处理
- MutationObserver 监听主题变化
- 动态侧边栏生成

### 3. 通用 Vue 3 风格
**适用场景**：通用 Vue 3 应用、工具组件
**参考来源**：Vue 3 官方文档和最佳实践

**主要特点**：
- Vue 3 Composition API
- TypeScript 类型安全
- Props/Emits 类型定义
- 组件通信模式

---

## Vue 后台管理系统代码风格规范

基于 `E:\working\website\NCHome\backend` 项目的实际代码，后台管理系统开发遵循以下风格规范：

### 1. 项目结构

```
backend/
├── src/
│   ├── main.ts                    # 应用入口
│   ├── permission.ts              # 路由权限控制
│   ├── App.vue                    # 根组件
│   ├── components/                # 可复用组件
│   │   ├── FormData.vue           # 表单数据组件
│   │   ├── dlgDrawer.vue          # 抽屉对话框
│   │   └── sIdentify.vue         # 验证码组件
│   ├── composables/               # 组合式函数（逻辑复用）
│   │   ├── api.ts                # API 请求封装
│   │   ├── axiosInstance.ts      # Axios 实例配置
│   │   ├── auth.ts               # 认证相关
│   │   ├── dbModInfo.ts         # 数据库模型信息
│   │   ├── settings.ts          # 配置文件
│   │   └── util.ts              # 工具函数
│   ├── layouts/                   # 布局组件
│   │   └── admin.vue            # 后台管理布局
│   ├── pages/                     # 页面（按功能模块分页）
│   │   ├── login.vue            # 登录页
│   │   ├── backend.vue          # 后台首页
│   │   ├── asset/              # 资产管理
│   │   ├── company/            # 公司管理
│   │   ├── customer/           # 客户管理
│   │   └── sale/               # 销售管理
│   ├── router/                    # 路由配置
│   │   └── index.ts
│   └── store/                     # Vuex 状态管理
│       └── index.ts
├── vite.config.ts                 # Vite 配置
├── tsconfig.json                  # TypeScript 配置
└── index.html                     # HTML 入口
```

### 2. 命名规范

| 类型 | 规范 | 示例 |
|------|------|------|
| 文件名 | 小驼峰 | `FormData.vue`, `axiosInstance.ts` |
| 组件名 | 大驼峰/帕斯卡命名 | `dbFormData`, `dlgDrawer`, `sIdentify` |
| 变量名 | 小驼峰，下划线分隔词组 | `asset_data`, `page_title`, `current_page` |
| 常量名 | 全大写下划线 | `CHUNK_SIZE`, `API_URL`, `MAX_RETRY` |
| 函数名 | 小驼峰，动词开头 | `handle_add`, `update_products`, `fetch_data` |
| 接口/类型 | 大驼峰，前缀 I | `interface RETRY_CONFIG`, `interface Product` |
| Props | 小驼峰，前缀 init_ | `init_page_title`, `init_columns` |

### 3. 组件模板

#### 3.1 基本组件结构

```vue
<template>
    <div class="component-name">
        <h1>{{ page_title }}</h1>

        <!-- Element Plus 表格 -->
        <el-table :data="displayed_data" border>
            <el-table-column
                v-for="(column, index) in columns"
                :key="index"
                :prop="column.prop"
                :label="column.label"
            />
        </el-table>

        <!-- 插槽 -->
        <slot name="custom-slot"></slot>
    </div>
</template>

<script lang="ts" setup>
import {ref, computed, watch, onMounted} from "vue";
import type {PropType} from "vue";

// Props 定义
const props = defineProps({
    init_page_title: {
        type: String,
        default: "默认标题"
    },
    init_columns: {
        type: Array as PropType<Column[]>,
        default: () => []
    },
    on_blur_handle: {
        type: Function,
        default: () => {}
    }
});

// Emits 定义
const emit = defineEmits<{
    update: [value: string];
    delete: [id: number];
}>();

// 响应式数据
const page_title = ref(props.init_page_title);
const current_page = ref(1);

// 计算属性
const displayed_data = computed(() => {
    return props.init_columns.filter((item) => item.visible);
});

// 监听器
watch(() => props.init_page_title, (newVal) => {
    page_title.value = newVal;
});

// 生命周期
onMounted(() => {
    console.log("组件已挂载");
});

// 方法
const handle_add = () => {
    emit("update", "新数据");
};

// 暴露给父组件
defineExpose({
    handle_add
});
</script>

<style scoped lang="css">
.component-name {
    padding: 20px;
}
</style>
```

### 4. Axios 封装

#### 4.1 基础配置

```typescript
import axios, {type AxiosInstance, type AxiosError} from "axios";
import config from "./settings";
import {get_token, remove_token} from "./auth";
import {useRouter} from 'vue-router';

// 请求重试配置接口
export interface RETRY_CONFIG {
    retry?: number; // 重试次数
    current_retry_attempt?: number; // 当前重试次数
    retry_delay?: number; // 初始重试延迟（毫秒）
    backoff_factor?: number; // 退避因子
    max_retry_delay?: number; // 最大重试延迟
    should_retry?: (error: AxiosError) => boolean; // 是否重试
}

// 增强 AxiosRequestConfig 类型
declare module "axios" {
    interface AxiosRequestConfig {
        _retryConfig?: RETRY_CONFIG;
    }
}

// 创建 Axios 实例
const axiosInstance: AxiosInstance = axios.create({
    baseURL: config.baseurl,
    timeout: 5000,
    headers: {
        "Content-Type": "application/json",
    },
});
```

#### 4.2 拦截器

```typescript
// 添加认证拦截器
function add_auth_interceptor(instance: AxiosInstance) {
    instance.interceptors.request.use(
        (request) => {
            const token = get_token();
            if (token) {
                request.headers["Authorization"] = `Bearer ${token}`;
            }
            return request;
        },
        (error) => Promise.reject(error)
    );

    instance.interceptors.response.use(
        (response) => response,
        async (error) => {
            if (error.response?.status === 401) {
                remove_token();
                const router = useRouter();
                await router.push("/login");
            }
            return Promise.reject(error);
        }
    );
}

// 添加重试拦截器（指数退避策略）
function add_retry_interceptor(instance: AxiosInstance, config: RETRY_CONFIG) {
    instance.interceptors.response.use(
        (response) => response,
        async (error) => {
            const {config: requestConfig} = error;
            const {
                retry = 3,
                current_retry_attempt = 0,
                retry_delay = 1000,
                backoff_factor = 2,
                max_retry_delay = 15000,
            } = requestConfig._retryConfig || config;

            if (current_retry_attempt >= retry) {
                return Promise.reject(error);
            }

            // 指数退避计算
            const delay = Math.min(
                retry_delay * Math.pow(backoff_factor, current_retry_attempt),
                max_retry_delay
            );

            await new Promise((resolve) => setTimeout(resolve, delay));

            const updatedConfig: RETRY_CONFIG = {
                ...config,
                current_retry_attempt: current_retry_attempt + 1,
            };

            return instance({
                ...requestConfig,
                _retryConfig: updatedConfig,
            });
        }
    );
}

// 应用拦截器
add_auth_interceptor(axiosInstance);
add_retry_interceptor(axiosInstance, {
    retry: 3,
    retry_delay: 1000,
    backoff_factor: 2,
    max_retry_delay: 15000,
});

export default axiosInstance;
```

### 5. API 请求封装

```typescript
import axiosInstance from "./axiosInstance";

// 响应数据接口
export interface API_RESPONSE<T> {
    data?: T;
    message?: string;
    code?: number;
}

// 资产列表接口
export interface ASSET_INFO {
    id?: number;
    name: string;
    version: string;
    description: string;
    price_original: string;
    price_pre: number;
}

// 获取资产列表
export async function get_asset_list(page: number = 1, page_size: number = 10) {
    const response = await axiosInstance.get<API_RESPONSE<ASSET_INFO[]>>(
        `/api/assets?page=${page}&page_size=${page_size}`
    );
    return response.data;
}

// 创建资产
export async function create_asset(asset: ASSET_INFO) {
    const response = await axiosInstance.post<API_RESPONSE<ASSET_INFO>>(
        "/api/assets",
        asset
    );
    return response.data;
}

// 删除资产
export async function delete_asset(id: number) {
    const response = await axiosInstance.delete<API_RESPONSE<void>>(
        `/api/assets/${id}`
    );
    return response.data;
}
```

### 6. Vuex 状态管理

```typescript
import {createStore} from "vuex";
import type {Store} from "vuex";

// 类型定义
interface State {
    token: string;
    user_info: USER_INFO | null;
    is_loading: boolean;
}

interface USER_INFO {
    id: number;
    name: string;
    email: string;
}

// 创建 Store
export const store = createStore<State>({
    state: {
        token: "",
        user_info: null,
        is_loading: false,
    },

    getters: {
        is_logged_in: (state) => !!state.token,
        user_name: (state) => state.user_info?.name || "",
    },

    mutations: {
        SET_TOKEN(state, token: string) {
            state.token = token;
        },
        SET_USER_INFO(state, user_info: USER_INFO) {
            state.user_info = user_info;
        },
        SET_LOADING(state, is_loading: boolean) {
            state.is_loading = is_loading;
        },
    },

    actions: {
        async login({commit}, credentials: {email: string; password: string}) {
            commit("SET_LOADING", true);
            try {
                const response = await login_api(credentials);
                commit("SET_TOKEN", response.token);
                commit("SET_USER_INFO", response.user_info);
            } finally {
                commit("SET_LOADING", false);
            }
        },
    },
});

export default store;
```

### 7. 路由配置

```typescript
import {createRouter, createWebHashHistory} from "vue-router";

const routes = [
    {
        path: "/",
        component: () => import("~/layouts/admin.vue"),
        children: [
            {
                path: "",
                redirect: "/backend",
            },
            {
                path: "backend",
                component: () => import("~/pages/backend.vue"),
                meta: {title: "后台首页"},
            },
            {
                path: "asset/list",
                component: () => import("~/pages/asset/list.vue"),
                meta: {title: "资产管理", requiresAuth: true},
            },
            {
                path: "company/list",
                component: () => import("~/pages/company/list.vue"),
                meta: {title: "公司管理", requiresAuth: true},
            },
        ],
    },
    {
        path: "/login",
        component: () => import("~/pages/login.vue"),
        meta: {title: "登录"},
    },
];

const router = createRouter({
    history: createWebHashHistory(),
    routes,
});

// 路由守卫
router.beforeEach((to, from, next) => {
    const token = localStorage.getItem("token");

    if (to.meta.requiresAuth && !token) {
        next("/login");
    } else {
        next();
    }
});

export default router;
```

### 8. Vite 配置

```typescript
import {defineConfig, loadEnv} from 'vite';
import vue from '@vitejs/plugin-vue'
import {resolve} from 'path';

const pathResolve = (dir: string) => resolve(__dirname, dir);

export default defineConfig(({mode}) => {
    const env = loadEnv(mode, resolve(__dirname, '..'), '');

    return {
        plugins: [
            vue(),
        ],

        resolve: {
            alias: {
                "~": pathResolve('src'),
            },
        },

        define: {
            'import.meta.env.VITE_APP_TITLE': JSON.stringify(env.VITE_APP_TITLE),
            'import.meta.env.VITE_API_URL': JSON.stringify(env.VITE_API_URL),
        },

        server: {
            proxy: {
                '/API': {
                    target: env.VITE_API_URL,
                    changeOrigin: true,
                    rewrite: (path) => path.replace(/^\/API/, ''),
                },
            },
            host: '192.168.31.156',
            port: 52481,
        },
    }
})
```

### 9. Element Plus 使用规范

```vue
<template>
    <el-container>
        <!-- 表单 -->
        <el-form ref="form_ref" :model="form_data" :rules="form_rules">
            <el-form-item label="名称" prop="name">
                <el-input v-model="form_data.name" placeholder="请输入名称">
                    <template #prefix>
                        <el-icon><MessageBox /></el-icon>
                    </template>
                </el-input>
            </el-form-item>

            <el-form-item label="开关" prop="is_active">
                <el-switch
                    v-model="form_data.is_active"
                    active-text="开启"
                    inactive-text="关闭"
                />
            </el-form-item>
        </el-form>

        <!-- 表格 -->
        <el-table :data="table_data" border>
            <el-table-column prop="name" label="名称" />
            <el-table-column label="操作">
                <template #default="scope">
                    <el-button @click="handle_edit(scope.row)">编辑</el-button>
                    <el-button @click="handle_delete(scope.row)" type="danger">删除</el-button>
                </template>
            </el-table-column>
        </el-table>

        <!-- 对话框 -->
        <el-dialog v-model="dialog_visible" title="编辑">
            <el-form :model="edit_data">
                <el-form-item label="名称">
                    <el-input v-model="edit_data.name" />
                </el-form-item>
            </el-form>
            <template #footer>
                <el-button @click="dialog_visible = false">取消</el-button>
                <el-button type="primary" @click="dialog_visible = false">确定</el-button>
            </template>
        </el-dialog>
    </el-container>
</template>
```

### 10. TypeScript 类型定义

```typescript
// 列配置接口
export interface Column {
    prop: string;
    label: string;
    sortable?: boolean;
    editable?: boolean;
    date?: boolean;
    is_boolean?: boolean;
    is_number?: boolean;
    precision?: number;
    width?: number;
    align?: 'left' | 'center' | 'right';
}

// 产品接口
export interface Product {
    id?: number;
    name: string;
    version: string;
    price: string;
    created_at?: string;
    is_editing?: boolean;
}

// 分页接口
export interface Pagination {
    current_page: number;
    page_size: number;
    total: number;
    total_pages: number;
}

// 表单数据接口
export interface FormData {
    name: string;
    email: string;
    phone?: string;
    is_active: boolean;
}
```

---

## VitePress 文档站点代码风格规范

基于 `E:\working\website\NCHome\docs` 项目的实际代码，VitePress 开发遵循以下风格规范：

### 1. 项目结构

```
docs/
├── .vuepress/                       # VitePress 配置目录
│   ├── config.ts                    # 主配置文件
│   ├── client.ts                    # 客户端增强
│   ├── sidebar.ts                   # 侧边栏配置
│   ├── navbar.ts                    # 导航栏配置
│   ├── plugins/                     # 自定义插件
│   │   ├── fileLinksPlugin.ts      # 文件链接插件
│   │   └── dynamicTitlePlugin.ts   # 动态标题插件
│   ├── theme/                       # 主题自定义
│   │   ├── layouts/               # 布局
│   │   │   └── Layout.vue
│   │   ├── components/            # 组件
│   │   ├── pages/                 # 页面组件
│   │   │   ├── NCHome.vue
│   │   │   ├── NCLogin.vue
│   │   │   └── ...
│   │   ├── store/                 # 状态管理
│   │   │   └── index.js
│   │   └── utils/                 # 工具函数
│   ├── styles/                      # 全局样式
│   └── public/                      # 公共资源
└── guide/                           # 文档内容
    ├── tools/                      # 产品介绍
    ├── demo/                       # 作品展示
    └── document/                   # 问题归类
```

### 2. 配置文件

```typescript
import {defineUserConfig} from "vuepress";
import {viteBundler} from "@vuepress/bundler-vite";
import {defaultTheme} from "@vuepress/theme-default";
import * as fs from 'fs';
import * as path from 'path';
import {getDirname} from "@vuepress/utils";

const __dirname = getDirname(import.meta.url);

// 自定义函数：从目录中获取组件
function getComponentsFromDir(dir: string, ext = ".vue") {
    const components = {};

    function readDir(currentPath: string) {
        const files = fs.readdirSync(currentPath);

        files.forEach((file: string) => {
            const fullPath = path.join(currentPath, file);
            const stat = fs.statSync(fullPath);

            if (stat.isDirectory()) {
                readDir(fullPath);
            } else if (stat.isFile() && path.extname(file) === ext) {
                const componentName = path.basename(file, ext);
                components[componentName] = fullPath;
            }
        });
    }

    readDir(dir);
    return components;
}

export default defineUserConfig({
    bundler: viteBundler(),

    lang: "zh-CN",
    title: "NCHome",
    description: "知识面过窄（北京）科技有限公司",

    alias: {
        "@theme": path.resolve(__dirname, "./theme"),
        "@components": path.resolve(__dirname, "./theme/components"),
        "@utils": path.resolve(__dirname, "./theme/utils"),
        "@styles": path.resolve(__dirname, "./styles"),
    },

    theme: defaultTheme({
        logo: "/images/logo.svg",
        navbar: navbarConfig,
        sidebar: sidebarConfig,
    }),

    plugins: [
        registerComponentsPlugin({
            components: {
                ...getComponentsFromDir(path.resolve(__dirname, "./theme/pages"), ".vue"),
            },
        }),
    ],
});
```

### 3. 自定义插件开发

```typescript
import type {Plugin} from "@vuepress/core";
import * as fs from 'fs';
import * as path from 'path';

export const fileLinksPlugin = ({
    defaultFileTypes = ['.md'],
    defaultDepth = 2,
}): Plugin => ({
    name: 'file-links-plugin',

    onInitialized: (app) => {
        // 在初始化时执行
        console.log('File links plugin initialized');
    },

    extendsPageData: (page, app) => {
        // 扩展页面数据
        const dir = path.dirname(page.filePath);
        const files = fs.readdirSync(dir);

        const links = files
            .filter(file => defaultFileTypes.includes(path.extname(file)))
            .map(file => ({
                name: path.basename(file, path.extname(file)),
                path: `/${path.relative(app.dir, path.join(dir, file))}`,
            }));

        page.frontmatter.fileLinks = links;
    },
});
```

### 4. 自定义主题组件

```vue
<template>
    <div class="custom-layout">
        <div class="vp-hero">
            <img class="vp-hero-image" :src="logo_icon" alt="Logo">
            <h1 id="main-title">{{ title }}</h1>
            <p class="vp-hero-description">{{ description }}</p>
        </div>
    </div>
</template>

<script setup lang="ts">
import {ref, onMounted, onBeforeUnmount} from "vue";

const logo_icon = ref("/images/logo.svg");
const title = ref("标题");
const description = ref("描述");

const updateLogoIcon = () => {
    const dataTheme = document.documentElement.getAttribute('data-theme');
    logo_icon.value = dataTheme === "light" ? "/images/logo.svg" : "/images/logo_dark.svg";
};

// 使用 MutationObserver 监听主题变化
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

<style scoped lang="css">
.vp-hero {
    padding: 40px;
    text-align: center;
}
</style>
```

---

## 通用 Vue 3 最佳实践

### 1. Composition API 使用

```vue
<script setup lang="ts">
import {ref, reactive, computed, watch, onMounted} from "vue";

// ref - 用于基本类型
const count = ref(0);
const message = ref("Hello");

// reactive - 用于对象
const user = reactive({
    name: "John",
    age: 30,
});

// computed - 计算属性
const fullName = computed(() => `${user.name} ${user.age}`);

// watch - 监听器
watch(count, (newVal, oldVal) => {
    console.log(`Count changed from ${oldVal} to ${newVal}`);
});

// onMounted - 生命周期
onMounted(() => {
    console.log("Component mounted");
});

// 方法
const increment = () => {
    count.value++;
};
</script>
```

### 2. Props 和 Emits 类型定义

```typescript
// Props
interface Props {
    title: string;
    count?: number;
    onUpdate?: (value: number) => void;
}

const props = withDefaults(defineProps<Props>(), {
    count: 0,
});

// Emits
interface Emits {
    (e: 'update', value: number): void;
    (e: 'delete', id: number): void;
}

const emit = defineEmits<Emits>();
```

### 3. 组件通信

```typescript
// 父组件
<template>
    <ChildComponent
        :title="page_title"
        @update="handle_update"
        @delete="handle_delete"
    />
</template>

// 子组件
const props = defineProps<{
    title: string;
}>();

const emit = defineEmits<{
    update: [value: string];
    delete: [id: number];
}>();

const handle_click = () => {
    emit("update", "新值");
};

// 暴露方法给父组件
defineExpose({
    exposed_method
});
```

### 4. 样式规范

```vue
<style scoped lang="css">
/* 使用 scoped 避免样式污染 */
.container {
    padding: 20px;
}

/* 深度选择器 */
.container :deep(.el-button) {
    margin-right: 10px;
}

/* 或使用 ::v-deep */
.container ::v-deep(.el-button) {
    margin-right: 10px;
}
</style>
```

---

## 代码风格检查清单

在生成或审查代码时，请确保：

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

---

## 参考资源

- [Vue 3 官方文档](https://vuejs.org/)
- [TypeScript 官方文档](https://www.typescriptlang.org/)
- [Vite 官方文档](https://vitejs.dev/)
- [VuePress 官方文档](https://vuepress.vuejs.org/)
- [Element Plus 官方文档](https://element-plus.org/)
