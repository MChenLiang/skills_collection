---
title: API 文档标题
description: API 功能描述
date: 2024-03-12
tags: [API, 接口, 文档]
categories: [API]
---

<h1 style="text-align: center;">API 文档标题</h1>
<el-divider border-style="dashed">
    <div> ~ API 接口文档 ~ </div>
</el-divider>

## 概述

简要描述 API 的功能和用途...

## 接口信息

- **接口名称**：API 名称
- **接口类型**：GET / POST / PUT / DELETE
- **接口路径**：/api/path
- **认证方式**：无需认证 / Token 认证

## 请求参数

### 请求头

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| Content-Type | string | 是 | application/json | 请求内容类型 |
| Authorization | string | 是 | - | 认证令牌 |

### 路径参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| id | string | 是 | 资源ID |

### 查询参数

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| page | number | 否 | 1 | 页码 |
| size | number | 否 | 10 | 每页数量 |

### 请求体

```json
{
  "field1": "value1",
  "field2": 123,
  "field3": {
    "nestedField": "nestedValue"
  }
}
```

**请求体说明**：...

## 响应数据

### 成功响应

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "field1": "value1",
    "field2": 123
  }
}
```

**响应说明**：...

### 响应字段说明

| 字段名 | 类型 | 说明 |
|--------|------|------|
| code | number | 响应状态码 |
| message | string | 响应消息 |
| data | object | 响应数据 |

### 错误响应

```json
{
  "code": 400,
  "message": "参数错误",
  "data": null
}
```

## 错误码

| 错误码 | 说明 |
|--------|------|
| 200 | 成功 |
| 400 | 参数错误 |
| 401 | 未认证 |
| 403 | 无权限 |
| 404 | 资源不存在 |
| 500 | 服务器错误 |

## 示例

### cURL 示例

```bash
curl -X GET "https://api.example.com/path?id=123" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer token"
```

### JavaScript 示例

```javascript
fetch('https://api.example.com/path?id=123', {
  method: 'GET',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer token'
  }
})
  .then(response => response.json())
  .then(data => console.log(data));
```

### Python 示例

```python
import requests

headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer token'
}

response = requests.get('https://api.example.com/path?id=123', headers=headers)
data = response.json()
print(data)
```

## 注意事项

::: warning 注意
- 必须进行认证
- 参数必须完整
- 注意接口频率限制
:::

## 更新日志

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| 1.0.0 | 2024-03-12 | 初始版本 |

<el-divider border-style="dashed">
  <div> · End · </div>
</el-divider>
