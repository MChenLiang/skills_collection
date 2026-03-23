import axios, {type AxiosInstance, type AxiosError} from "axios";
import config from "./settings";
import {get_token, remove_token} from "./auth";
import {useRouter} from 'vue-router';


/**
 * 请求重试配置接口
 */
export interface RETRY_CONFIG {
    retry?: number; // 指定重试请求的次数
    current_retry_attempt?: number; // 当前重试次数
    retry_delay?: number; // 初始重试延迟时间（毫秒）
    backoff_factor?: number; // 退避因子，用于指数退避
    max_retry_delay?: number; // 最大重试延迟时间
    instance?: AxiosInstance; // Axios 实例
    http_method_store_try?: string[]; // 自动重试的 HTTP 方法
    status_code_store_try?: number[][]; // 重试的 HTTP 状态码范围
    on_retry_attempt?: (error: AxiosError) => void; // 每次重试时的回调函数
    should_retry?: (error: AxiosError) => boolean; // 是否重试的判断函数
    no_response_retries?: number; // 无响应重试次数
    check_retry_after?: boolean; // 是否检查 Retry-After 头
    max_retry_after?: number; // 最大 Retry-After 时间
}

// 增强 AxiosRequestConfig 类型以支持自定义字段
declare module "axios" {
    interface AxiosRequestConfig {
        _retryConfig?: RETRY_CONFIG;
    }
}

/**
 * 创建 Axios 实例
 */
const axiosInstance: AxiosInstance = axios.create({
    baseURL: config.baseurl,
    timeout: 5000,
    headers: {
        "Content-Type": "application/json",
    },
});

/**
 * 添加认证拦截器
 * 自动在请求头中添加 Bearer Token
 */
function add_auth_interceptor(instance: AxiosInstance) {
    // 请求拦截器
    instance.interceptors.request.use(
        (request) => {
            const token = get_token();
            if (token) {
                request.headers["Authorization"] = `Bearer ${token}`;
            }
            return request;
        },
        // 请求错误时直接抛出
        (error) => Promise.reject(error)
    );

    // 响应拦截器
    instance.interceptors.response.use(
        (response) => response,
        async (error) => {
            // 处理 401 错误（未授权）
            if (error.response?.status === 401) {
                remove_token();
                const router = useRouter();
                await router.push("/login");
            }
            return Promise.reject(error);
        }
    );
}

/**
 * 添加重试拦截器
 * 实现指数退避重试策略
 */
function add_retry_interceptor(instance: AxiosInstance, config: RETRY_CONFIG) {
    instance.interceptors.response.use(
        (response) => response,
        async (error) => {
            const {config: requestConfig} = error;

            if (!requestConfig) {
                return Promise.reject(error);
            }

            const {
                retry = 3,
                current_retry_attempt = 0,
                retry_delay = 1000,
                backoff_factor = 2,
                max_retry_delay = 15000,
                should_retry = default_should_retry,
                on_retry_attempt,
                check_retry_after = true,
                max_retry_after = 60000,
            } = requestConfig._retryConfig || config;

            // 如果达到最大重试次数或者不满足重试条件，拒绝请求
            if (current_retry_attempt >= retry || !should_retry(error)) {
                return Promise.reject(error);
            }

            // 调用回调函数，记录重试日志或其他操作
            if (on_retry_attempt) {
                console.log(`[Retry] Attempt ${current_retry_attempt + 1} for URL: ${requestConfig.url}`);
                on_retry_attempt(error);
            }

            // 检查 Retry-After 响应头
            let delay = retry_delay * Math.pow(backoff_factor, current_retry_attempt);
            if (check_retry_after && error.response?.headers['retry-after']) {
                const retryAfter = parseInt(error.response.headers['retry-after'], 10) * 1000;
                delay = Math.min(retryAfter, max_retry_after, delay);
            }
            if (delay > max_retry_delay) {
                delay = max_retry_delay;
            }

            // 延迟指定时间后重试
            await new Promise((resolve) => setTimeout(resolve, delay));

            // 更新重试配置
            const updatedConfig: RETRY_CONFIG = {
                ...config,
                current_retry_attempt: current_retry_attempt + 1,
            };

            // 重新发起请求，并传递更新后的重试配置
            return instance({
                ...requestConfig,
                _retryConfig: updatedConfig,
            });
        }
    );
}

/**
 * 默认的重试判断逻辑
 */
function default_should_retry(error: AxiosError): boolean {
    const {response, code, message} = error;

    // 超时或网络错误
    if (code === 'ECONNABORTED' || message.includes('timeout')) {
        return true;
    }

    // 无响应时重试
    if (!response) {
        return true;
    }

    // 针对 5xx 错误的重试
    return response.status >= 500 && response.status < 600;
}

/**
 * 应用拦截器
 */
const retry_config: RETRY_CONFIG = {
    retry: 3,
    retry_delay: 1000,
    backoff_factor: 2,
    max_retry_delay: 15000,
    should_retry: default_should_retry,
    check_retry_after: true,
};

add_auth_interceptor(axiosInstance);
add_retry_interceptor(axiosInstance, retry_config);

export default axiosInstance;
