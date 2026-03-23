<template>
    <div class="page-container">
        <h1 class="page-title">{{ page_title }}</h1>
        <hr/>

        <!-- 顶部操作区域 -->
        <div class="top-section">
            <el-input
                v-model="search_keyword"
                placeholder="搜索关键词"
                clearable
                style="width: 300px; margin-right: 10px;"
                @clear="handle_search"
            >
                <template #prefix>
                    <el-icon><Search /></el-icon>
                </template>
            </el-input>
            <el-button type="primary" @click="handle_search">搜索</el-button>
            <el-button @click="handle_refresh">刷新</el-button>
        </div>

        <!-- 数据表格 -->
        <div class="data-section">
            <el-table
                :data="displayed_data"
                border
                ref="table_ref"
                @row-click="on_row_click"
                @row-dblclick="on_row_double_click"
                class="data-table"
                :row-class-name="row_class_name"
                v-loading="is_loading"
            >
                <el-table-column type="selection" width="55" />

                <el-table-column
                    v-for="(column, index) in columns"
                    :key="index"
                    :prop="column.prop"
                    :label="column.label"
                    :sortable="column.sortable"
                    :width="column.width"
                    :align="column.align || 'left'"
                    show-overflow-tooltip
                >
                    <template #default="scope">
                        <!-- 日期列 -->
                        <span v-if="column.date">
                            {{ format_date(scope.row[column.prop]) }}
                        </span>

                        <!-- 布尔列 -->
                        <el-tag
                            v-else-if="column.is_boolean"
                            :type="scope.row[column.prop] ? 'success' : 'info'"
                        >
                            {{ scope.row[column.prop] ? '是' : '否' }}
                        </el-tag>

                        <!-- 数字列 -->
                        <span v-else-if="column.is_number">
                            {{ format_number(scope.row[column.prop], column.precision) }}
                        </span>

                        <!-- 普通列 -->
                        <span v-else>
                            {{ scope.row[column.prop] }}
                        </span>
                    </template>
                </el-table-column>

                <!-- 操作列 -->
                <el-table-column label="操作" width="200" fixed="right">
                    <template #default="scope">
                        <el-button
                            size="small"
                            @click="handle_edit(scope.row)"
                        >
                            编辑
                        </el-button>
                        <el-button
                            size="small"
                            type="danger"
                            @click="handle_delete(scope.row)"
                        >
                            删除
                        </el-button>
                    </template>
                </el-table-column>
            </el-table>
        </div>

        <!-- 分页区域 -->
        <div class="pagination-section">
            <div class="pagination-info">
                <span>共 {{ total }} 条记录</span>
            </div>
            <div class="pagination-controls">
                <el-select
                    v-model="page_size"
                    size="small"
                    style="width: 100px; margin-right: 10px;"
                    @change="handle_page_size_change"
                >
                    <el-option
                        v-for="item in [10, 20, 30, 50, 100]"
                        :key="item"
                        :label="`${item}条/页`"
                        :value="item"
                    />
                </el-select>
                <span>第 {{ current_page }} 页，共 {{ total_pages }} 页</span>
                <el-button
                    @click="prev_page"
                    :disabled="current_page === 1"
                    size="small"
                >
                    上一页
                </el-button>
                <el-button
                    @click="next_page"
                    :disabled="current_page === total_pages"
                    size="small"
                >
                    下一页
                </el-button>
            </div>
        </div>

        <!-- 编辑对话框 -->
        <el-dialog
            v-model="dialog_visible"
            :title="dialog_title"
            width="40%"
            @close="handle_dialog_close"
        >
            <el-form
                ref="form_ref"
                :model="form_data"
                :rules="form_rules"
                label-width="100px"
            >
                <el-form-item label="名称" prop="name">
                    <el-input
                        v-model="form_data.name"
                        placeholder="请输入名称"
                    >
                        <template #prefix>
                            <el-icon><MessageBox /></el-icon>
                        </template>
                    </el-input>
                </el-form-item>

                <el-form-item label="版本" prop="version">
                    <el-input
                        v-model="form_data.version"
                        placeholder="请输入版本号"
                    >
                        <template #prefix>
                            <el-icon><Lock /></el-icon>
                        </template>
                    </el-input>
                </el-form-item>

                <el-form-item label="描述" prop="description">
                    <el-input
                        v-model="form_data.description"
                        type="textarea"
                        :rows="3"
                        placeholder="请输入描述"
                    />
                </el-form-item>

                <el-form-item label="价格" prop="price">
                    <el-input-number
                        v-model="form_data.price"
                        :min="0"
                        :precision="2"
                        :step="0.01"
                        controls-position="right"
                    >
                        <template #prefix>￥</template>
                    </el-input-number>
                </el-form-item>

                <el-form-item label="是否启用" prop="is_active">
                    <el-switch
                        v-model="form_data.is_active"
                        active-text="启用"
                        inactive-text="禁用"
                    />
                </el-form-item>
            </el-form>

            <template #footer>
                <el-button @click="dialog_visible = false">取消</el-button>
                <el-button type="primary" @click="handle_submit" :loading="is_saving">
                    确定
                </el-button>
            </template>
        </el-dialog>
    </div>
</template>

<script lang="ts" setup>
import {ref, reactive, computed, onMounted, type PropType} from "vue";
import {ElMessage, ElMessageBox} from "element-plus";
import {dayjs} from "element-plus";
import type {Column, Product} from "~/composables/dbModInfo";

// Props 定义
const props = defineProps({
    init_page_title: {
        type: String,
        default: "基础数据界面"
    },
    init_columns: {
        type: Array as PropType<Column[]>,
        default: () => []
    },
    init_api_endpoint: {
        type: String,
        default: "/api/products"
    }
});

// 响应式数据
const page_title = ref(props.init_page_title);
const search_keyword = ref("");
const current_page = ref(1);
const page_size = ref(10);
const total = ref(0);
const is_loading = ref(false);
const is_saving = ref(false);

// 表格数据
const table_data = ref<Product[]>([]);
const selected_rows = ref<Product[]>([]);

// 对话框相关
const dialog_visible = ref(false);
const dialog_title = ref("新增");
const is_edit_mode = ref(false);

// 表单数据
const form_data = reactive({
    id: 0,
    name: "",
    version: "",
    description: "",
    price: 0,
    is_active: true
});

// 表单校验规则
const form_rules = {
    name: [
        {required: true, message: "请输入名称", trigger: "blur"},
        {min: 2, max: 50, message: "长度在 2 到 50 个字符", trigger: "blur"}
    ],
    version: [
        {required: true, message: "请输入版本号", trigger: "blur"},
        {pattern: /^\d+\.\d+\.\d+$/, message: "格式：x.x.x", trigger: "blur"}
    ],
    price: [
        {required: true, message: "请输入价格", trigger: "blur"},
        {type: "number", min: 0, message: "价格不能小于 0", trigger: "blur"}
    ]
};

// Ref
const table_ref = ref();
const form_ref = ref();

// 计算属性
const displayed_data = computed(() => {
    if (!search_keyword.value) {
        return table_data.value;
    }
    const keyword = search_keyword.value.toLowerCase();
    return table_data.value.filter(item =>
        item.name.toLowerCase().includes(keyword)
    );
});

const total_pages = computed(() => {
    return Math.ceil(total.value / page_size.value);
});

// 方法
const fetch_data = async () => {
    is_loading.value = true;
    try {
        // 模拟 API 请求
        await new Promise(resolve => setTimeout(resolve, 500));
        // TODO: 替换为实际的 API 请求
        // const response = await api.get(props.init_api_endpoint, {
        //     params: {page: current_page.value, page_size: page_size.value}
        // });

        // 模拟数据
        table_data.value = [
            {
                id: 1,
                name: "产品 A",
                version: "1.0.0",
                description: "产品 A 描述",
                price: "99.00",
                created_at: new Date().toISOString(),
                is_editing: false
            }
        ] as any;
        total.value = 1;

    } catch (error) {
        ElMessage.error("获取数据失败");
    } finally {
        is_loading.value = false;
    }
};

const handle_search = () => {
    current_page.value = 1;
    fetch_data();
};

const handle_refresh = () => {
    search_keyword.value = "";
    current_page.value = 1;
    fetch_data();
};

const on_row_click = (row: Product) => {
    console.log("Row clicked:", row);
};

const on_row_double_click = (row: Product) => {
    handle_edit(row);
};

const row_class_name = ({row}: {row: Product}) => {
    return row.is_editing ? "editing-row" : "";
};

const handle_edit = (row: Product) => {
    is_edit_mode.value = true;
    dialog_title.value = "编辑";
    Object.assign(form_data, row);
    dialog_visible.value = true;
};

const handle_delete = async (row: Product) => {
    try {
        await ElMessageBox.confirm(
            `确定要删除 "${row.name}" 吗？`,
            "提示",
            {
                confirmButtonText: "确定",
                cancelButtonText: "取消",
                type: "warning",
            }
        );

        // TODO: 调用删除 API
        ElMessage.success("删除成功");
        fetch_data();
    } catch (error) {
        // 用户取消
    }
};

const handle_submit = async () => {
    if (!form_ref.value) return;

    await form_ref.value.validate(async (valid: boolean) => {
        if (!valid) return;

        is_saving.value = true;
        try {
            // TODO: 调用保存 API
            await new Promise(resolve => setTimeout(resolve, 500));

            ElMessage.success(is_edit_mode.value ? "更新成功" : "创建成功");
            dialog_visible.value = false;
            fetch_data();
        } catch (error) {
            ElMessage.error("保存失败");
        } finally {
            is_saving.value = false;
        }
    });
};

const handle_dialog_close = () => {
    form_ref.value?.resetFields();
};

const prev_page = () => {
    if (current_page.value > 1) {
        current_page.value--;
        fetch_data();
    }
};

const next_page = () => {
    if (current_page.value < total_pages.value) {
        current_page.value++;
        fetch_data();
    }
};

const handle_page_size_change = () => {
    current_page.value = 1;
    fetch_data();
};

const format_date = (date_str: string) => {
    return dayjs(date_str).format("YYYY-MM-DD HH:mm:ss");
};

const format_number = (value: number, precision: number = 2) => {
    return Number(value).toFixed(precision);
};

// 生命周期
onMounted(() => {
    fetch_data();
});

// 暴露给父组件
defineExpose({
    fetch_data,
    refresh: handle_refresh
});
</script>

<style scoped lang="css">
.page-container {
    padding: 20px;
}

.page-title {
    margin-bottom: 20px;
    color: #303133;
}

.top-section {
    margin-bottom: 20px;
    display: flex;
    align-items: center;
}

.data-section {
    margin-bottom: 20px;
}

.data-table {
    width: 100%;
}

.pagination-section {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 0;
}

.pagination-info {
    color: #606266;
}

.pagination-controls {
    display: flex;
    align-items: center;
    gap: 10px;
}

.editing-row {
    background-color: #fdf6ec;
}
</style>
