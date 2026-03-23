<template>
    <div class="custom-page">
        <!-- 英雄区域 -->
        <div class="vp-hero">
            <img class="vp-hero-image" :src="logo_icon" :alt="site_title">
            <h1 id="main-title">{{ site_title }}</h1>
            <p class="vp-hero-description">{{ site_description }}</p>
        </div>

        <!-- 功能区域 -->
        <div class="vp-features">
            <div
                v-for="(feature, index) in features"
                :key="index"
                class="vp-feature"
            >
                <h2>{{ feature.title }}</h2>
                <p>{{ feature.description }}</p>
            </div>
        </div>

        <el-divider border-style="dashed" style="height: 2.2rem"/>

        <!-- 按钮区域 -->
        <div class="action-section">
            <a href="/guide/tools/" class="btn btn-primary">开始探索 →</a>
            <a href="/guide/document/" class="btn btn-secondary">查看文档</a>
        </div>

        <!-- 视频播放器 -->
        <div class="video-section" v-if="video_url">
            <video-player
                :src="video_url"
                :poster="video_poster"
                :autoplay="false"
                :controls="true"
            />
        </div>
    </div>
</template>

<script setup lang="ts">
import {ref, onMounted, onBeforeUnmount} from "vue";

// 响应式数据
const logo_icon = ref("/images/logo.svg");
const site_title = ref("知识面过窄（北京）科技有限公司");
const site_description = ref("~ 科技使人进步 ~");
const video_url = ref("");
const video_poster = ref("");

// 功能列表
const features = ref([
    {
        title: "软件插件开发",
        description: "针对设计师和开发者面临的痛点，我们精心打造高效、易用的软件插件以及流程，助力他们突破创作瓶颈，提升工作效率。"
    },
    {
        title: "三维资产",
        description: "从细腻的模型到震撼的动画特效，我们为客户量身定制高品质的三维资产，满足多样化的创作需求。"
    },
    {
        title: "技术研发",
        description: "我们紧跟技术发展的步伐，持续投入研发，为行业带来颠覆性的创新成果。"
    }
]);

// 主题切换相关
const updateLogoIcon = () => {
    const dataTheme = document.documentElement.getAttribute('data-theme');
    logo_icon.value = dataTheme === "light"
        ? "/images/logo.svg"
        : "/images/logo_dark.svg";
};

// 使用 MutationObserver 监听主题变化
let observer: MutationObserver;

onMounted(() => {
    // 初始化图标
    updateLogoIcon();

    // 设置 MutationObserver 监听 data-theme 属性变化
    observer = new MutationObserver(updateLogoIcon);
    observer.observe(document.documentElement, {
        attributes: true,
        attributeFilter: ['data-theme']
    });

    // 初始化视频（如果有）
    // TODO: 根据实际需求加载视频
    // loadVideo();
});

onBeforeUnmount(() => {
    // 清理 MutationObserver
    if (observer) {
        observer.disconnect();
    }
});

// 视频加载（示例）
const loadVideo = async () => {
    try {
        // const response = await fetch('/api/video/info');
        // const data = await response.json();
        // video_url.value = data.url;
        // video_poster.value = data.poster;
    } catch (error) {
        console.error("加载视频失败:", error);
    }
};
</script>

<style scoped lang="css">
.custom-page {
    padding: 20px;
    max-width: 1200px;
    margin: 0 auto;
}

/* 英雄区域 */
.vp-hero {
    text-align: center;
    padding: 60px 20px;
    margin-bottom: 40px;
}

.vp-hero-image {
    width: 120px;
    height: 120px;
    margin-bottom: 20px;
    transition: all 0.3s ease;
}

.vp-hero-image:hover {
    transform: scale(1.1);
}

#main-title {
    font-size: 3rem;
    font-weight: 700;
    color: var(--vp-c-text-1);
    margin-bottom: 16px;
}

.vp-hero-description {
    font-size: 1.5rem;
    color: var(--vp-c-text-2);
    margin-top: 0;
}

/* 功能区域 */
.vp-features {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 24px;
    margin-bottom: 48px;
    padding: 0 20px;
}

.vp-feature {
    padding: 24px;
    border-radius: 8px;
    background-color: var(--vp-c-bg-soft);
    transition: all 0.3s ease;
}

.vp-feature:hover {
    transform: translateY(-4px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.vp-feature h2 {
    font-size: 1.5rem;
    font-weight: 600;
    margin: 0 0 12px 0;
    color: var(--vp-c-text-1);
}

.vp-feature p {
    margin: 0;
    color: var(--vp-c-text-2);
    line-height: 1.6;
}

/* 按钮区域 */
.action-section {
    text-align: center;
    margin: 48px 0;
}

.btn {
    display: inline-block;
    padding: 12px 32px;
    margin: 0 10px;
    font-size: 1rem;
    font-weight: 600;
    border-radius: 8px;
    text-decoration: none;
    transition: all 0.3s ease;
}

.btn-primary {
    background-color: var(--vp-c-brand);
    color: #fff;
}

.btn-primary:hover {
    background-color: var(--vp-c-brand-dark);
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(67, 97, 238, 0.3);
}

.btn-secondary {
    background-color: var(--vp-c-bg-soft);
    color: var(--vp-c-text-1);
    border: 1px solid var(--vp-c-border);
}

.btn-secondary:hover {
    background-color: var(--vp-c-bg-mute);
    transform: translateY(-2px);
}

/* 视频区域 */
.video-section {
    margin: 48px 0;
    padding: 0 20px;
}

/* 暗色模式适配 */
html[data-theme="dark"] .vp-feature {
    background-color: var(--vp-c-bg-soft);
}

/* 响应式设计 */
@media (max-width: 768px) {
    #main-title {
        font-size: 2rem;
    }

    .vp-hero-description {
        font-size: 1.2rem;
    }

    .vp-features {
        grid-template-columns: 1fr;
    }

    .btn {
        display: block;
        margin: 10px auto;
        width: 80%;
    }
}
</style>
