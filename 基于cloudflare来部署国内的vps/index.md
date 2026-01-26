# 基于cloudflare来部署国内的vps


# 使用 Cloudflare Tunnel 绕过国内域名备案限制

## 背景

当你的域名未备案，但服务器部署在国内（如腾讯云、阿里云）时，通过 Cloudflare CDN 代理访问会遇到以下问题：

```
用户 → Cloudflare CDN → 回源到国内服务器 → 被拦截（域名未备案）
```

即使 Cloudflare 开启了 Proxy 和 SSL，回源时仍会被国内云厂商拦截，返回 `525` 错误或跳转到备案提示页。

## 解决方案：Cloudflare Tunnel

Cloudflare Tunnel 的原理是**反向建立连接**：

```
传统方式：Cloudflare → 入站连接到你的服务器 → 被拦截
Tunnel：  你的服务器 → 主动出站连接到 Cloudflare → 不被拦截
```

因为是服务器**主动向外连接**，属于出站流量，不会触发备案检查。

## 实操步骤

### 1. 安装 cloudflared

```bash
# Debian/Ubuntu
curl -L https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb -o cloudflared.deb
dpkg -i cloudflared.deb

# CentOS/RHEL
curl -L https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.rpm -o cloudflared.rpm
rpm -i cloudflared.rpm

# 验证安装
cloudflared version
```

### 2. 登录 Cloudflare

```bash
cloudflared tunnel login
```

执行后会输出一个 URL，复制到浏览器打开，选择你的域名进行授权。授权成功后会在 `~/.cloudflared/` 生成 `cert.pem`。

### 3. 创建 Tunnel

```bash
cloudflared tunnel create my-tunnel
```

记住输出的 Tunnel ID（类似 `e68531cc-f521-4f8e-bd53-cd1a697993d3`）。

### 4. 配置 Tunnel

创建配置文件 `~/.cloudflared/config.yml`：

注意有些配置文件：**`/etc/cloudflared/config.yml` 里没有 `xx.xxx.xyz` 的配置！**

你之前看的是 `~/.cloudflared/config.yml`，但 systemd 服务用的是 `/etc/cloudflared/config.yml`。

```yaml
tunnel: <你的Tunnel-ID>
credentials-file: /root/.cloudflared/<你的Tunnel-ID>.json

ingress:
  - hostname: your-domain.com
    service: http://localhost:8080
  - service: http_status:404
```

- `hostname`: 你要代理的域名
- `service`: 本地服务地址（Nginx/应用监听的端口）

### 5. 配置 DNS

```bash
cloudflared tunnel route dns my-tunnel your-domain.com
```

这会自动在 Cloudflare DNS 中添加一条 CNAME 记录，指向你的 Tunnel。

### 6. 测试运行

```bash
cloudflared tunnel run my-tunnel
```

看到 `Registered tunnel connection` 表示连接成功。

### 7. 配置开机自启

```bash
cloudflared service install
```

一条命令搞定！它会：
- 复制配置到 `/etc/cloudflared/config.yml`
- 创建 systemd 服务
- 启动服务并设置开机自启

### 8. 验证

```bash
# 查看服务状态
systemctl status cloudflared

# 查看日志
journalctl -u cloudflared -f

# 测试访问
curl https://your-domain.com
```

## 常用命令

```bash
# 服务管理
systemctl start cloudflared
systemctl stop cloudflared
systemctl restart cloudflared

# 查看所有 Tunnel
cloudflared tunnel list

# 删除 Tunnel
cloudflared tunnel delete my-tunnel

# 卸载服务
cloudflared service uninstall
```

## 多域名配置

一个 Tunnel 可以代理多个域名：

```yaml
tunnel: <Tunnel-ID>
credentials-file: /root/.cloudflared/<Tunnel-ID>.json

ingress:
  - hostname: api.example.com
    service: http://localhost:5000
  - hostname: web.example.com
    service: http://localhost:3000
  - hostname: "*.example.com"
    service: http://localhost:8080
  - service: http_status:404
```

记得为每个域名添加 DNS 路由：

```bash
cloudflared tunnel route dns my-tunnel api.example.com
cloudflared tunnel route dns my-tunnel web.example.com
```

## 注意事项

1. **Cloudflare DNS 托管**：域名必须托管在 Cloudflare DNS 上
2. **出站网络**：服务器需要能访问外网（出站 443 端口）
3. **本地服务**：Tunnel 代理的是本地服务，确保本地端口正常监听
4. **免费额度**：Cloudflare Tunnel 基础功能免费，无流量限制

## 总结

| 对比项   | 传统 CDN 代理               | Cloudflare Tunnel           |
| -------- | --------------------------- | --------------------------- |
| 连接方向 | Cloudflare → 服务器（入站） | 服务器 → Cloudflare（出站） |
| 备案检查 | 会触发                      | 不触发                      |
| 开放端口 | 需要开放 80/443             | 无需开放任何入站端口        |
| 暴露 IP  | 可能泄露                    | 完全隐藏                    |

Cloudflare Tunnel 是目前绕过国内备案限制最优雅的方案，同时还能获得更好的安全性。

