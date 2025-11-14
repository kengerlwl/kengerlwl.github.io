---
title: HttpInterceptor隐私政策
top: false
cover: false
toc: true
mathjax: true
date: 2025-11-13 15:27:31
password:
summary:
tags:
- 隐私
categories:
- 声明相关文档
---

# 隐私政策 (Privacy Policy)

**最后更新日期 (Last Updated): 2025年11月14日**

## 中文版本

### 1. 概述

HTTP Request Interceptor（以下简称"本扩展"）是一个 Chrome 浏览器扩展程序，用于拦截和修改 HTTP 请求，方便前端开发调试。本隐私政策说明了本扩展如何收集、使用和保护用户数据。

### 2. 收集的数据

本扩展**仅在本地收集和处理**以下数据：

#### 2.1 HTTP 请求数据
- **URL**：被拦截的请求地址
- **HTTP 方法**：GET、POST、PUT、DELETE、PATCH 等
- **请求头 (Headers)**：包括 Content-Type、Authorization 等
- **请求体 (Body)**：POST/PUT 等请求的数据内容
- **响应数据**：服务器返回的响应内容

#### 2.2 用户交互数据
- 用户对请求的修改操作
- 用户的启用/禁用扩展操作
- 用户的编辑和发送请求操作

### 3. 数据使用方式

本扩展收集的数据**仅用于以下目的**：

1. **实时显示**：在扩展弹出窗口中显示拦截的请求列表
2. **请求修改**：允许用户编辑和修改 HTTP 请求
3. **功能实现**：实现请求拦截、暂停、修改和重新发送等核心功能
4. **用户体验**：保存用户的操作状态和偏好设置

### 4. 数据存储位置

- **所有数据均存储在用户的本地计算机上**
- 数据存储在浏览器的 `chrome.storage.local` 中
- **不会将任何数据上传到远程服务器**
- **不会与任何第三方共享数据**

### 5. 数据安全

- 本扩展不连接到任何外部服务器
- 所有数据处理都在用户的浏览器中进行
- 用户可以随时卸载扩展以删除所有本地数据

### 6. 第三方共享

**本扩展不与任何第三方共享用户数据**，包括：
- 不与分析服务共享数据
- 不与广告服务共享数据
- 不与其他扩展共享数据
- 不将数据发送到任何远程服务器

### 7. 用户权利

用户拥有以下权利：

1. **访问权**：用户可以查看扩展收集的所有数据
2. **删除权**：用户可以随时卸载扩展以删除所有数据
3. **控制权**：用户可以通过启用/禁用扩展来控制数据收集

### 8. 权限说明

本扩展请求以下 Chrome 权限及其用途：

| 权限 | 用途 |
|------|------|
| `webRequest` | 拦截和修改 HTTP 请求 |
| `webRequestBlocking` | 暂停请求以等待用户确认 |
| `storage` | 在本地存储请求数据和用户设置 |
| `tabs` | 获取当前标签页信息 |
| `activeTab` | 在活跃标签页中运行脚本 |
| `scripting` | 向网页注入脚本以拦截请求 |

### 9. 政策变更

如果本隐私政策发生变更，我们将在本页面更新最后修改日期。继续使用本扩展即表示您同意更新后的隐私政策。

### 10. 联系方式

如对本隐私政策有任何疑问，请通过以下方式联系：
- 提交 GitHub Issue
- 发送电子邮件至开发者

---

## English Version

### 1. Overview

HTTP Request Interceptor (hereinafter referred to as "this Extension") is a Chrome browser extension designed to intercept and modify HTTP requests for convenient front-end development and debugging. This Privacy Policy explains how this Extension collects, uses, and protects user data.

### 2. Data Collection

This Extension **only collects and processes data locally** as follows:

#### 2.1 HTTP Request Data
- **URL**: The address of intercepted requests
- **HTTP Method**: GET, POST, PUT, DELETE, PATCH, etc.
- **Request Headers**: Including Content-Type, Authorization, etc.
- **Request Body**: Data content of POST/PUT requests
- **Response Data**: Response content returned by the server

#### 2.2 User Interaction Data
- User modifications to requests
- User enable/disable operations
- User edit and send request operations

### 3. Data Usage

The data collected by this Extension is **used only for the following purposes**:

1. **Real-time Display**: Display the list of intercepted requests in the extension popup window
2. **Request Modification**: Allow users to edit and modify HTTP requests
3. **Feature Implementation**: Implement core functions such as request interception, pause, modification, and resending
4. **User Experience**: Save user operation states and preference settings

### 4. Data Storage Location

- **All data is stored on the user's local computer**
- Data is stored in the browser's `chrome.storage.local`
- **No data is uploaded to remote servers**
- **No data is shared with any third parties**

### 5. Data Security

- This Extension does not connect to any external servers
- All data processing is performed within the user's browser
- Users can uninstall the Extension at any time to delete all local data

### 6. Third-Party Sharing

**This Extension does not share user data with any third parties**, including:
- No sharing with analytics services
- No sharing with advertising services
- No sharing with other extensions
- No data transmission to any remote servers

### 7. User Rights

Users have the following rights:

1. **Access Right**: Users can view all data collected by the Extension
2. **Deletion Right**: Users can uninstall the Extension at any time to delete all data
3. **Control Right**: Users can control data collection by enabling/disabling the Extension

### 8. Permissions Explanation

This Extension requests the following Chrome permissions and their purposes:

| Permission | Purpose |
|-----------|---------|
| `webRequest` | Intercept and modify HTTP requests |
| `webRequestBlocking` | Pause requests to wait for user confirmation |
| `storage` | Store request data and user settings locally |
| `tabs` | Get current tab information |
| `activeTab` | Run scripts in active tabs |
| `scripting` | Inject scripts into web pages to intercept requests |

### 9. Policy Changes

If this Privacy Policy is modified, we will update the last modification date on this page. Continued use of this Extension indicates your acceptance of the updated Privacy Policy.

### 10. Contact

If you have any questions about this Privacy Policy, please contact us through:
- Submit a GitHub Issue
- Send an email to the developer

---

**声明 (Declaration)**: 本扩展完全尊重用户隐私，不收集任何个人信息，不进行任何跟踪，不与任何第三方共享数据。
