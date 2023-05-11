---
title: Caddy设置反向代理
urlname: bfza8bkx6884y40t
date: '2023-04-28 10:50:16 +0800'
tags:
  - caddy
categories: []
toc: true
---

# 简介

caddy 是使用 go 语言实现的一个高性能的类似于 nginx 的 HTTP 和反向代理服务器。支持自动申请 https 证书，配置也相当的精简
官网：[https://caddyserver.com/](https://caddyserver.com/)

# 代理服务器配置

caddy 的文档主要都是英文的
[https://caddyserver.com/docs/quick-starts/reverse-proxy](https://caddyserver.com/docs/quick-starts/reverse-proxy)
[https://caddyserver.com/docs/caddyfile/directives/reverse_proxy](https://caddyserver.com/docs/caddyfile/directives/reverse_proxy#headers)
第二个链接是详细的配置规则，文档很多，需要耐心下来慢慢的看才能很好的理解，我第一遍看的很快，完全没懂。吃完午饭之后，拿起手机慢悠悠的，一个句子一个句子的看，这才真的理解

caddy 的配置文件叫 Caddyfile
默认的 Header 都已经设置了 X-Forwarded-For X-Forwarded-Proto X-Forwarded-Host

```bash
# 代理本地的HTTP服务, eg: "https://example.com" -> localhost:4000
blog.devsleep.com {
	reverse_proxy localhost:4000
}

# 代理HTTPS需要注意修改Host才行
# header_up是请求时修改Header字段的意思
blog.devsleep.com {
  reverse_proxy blog.devsleep.com {
  	header_up Host {upstream_hostport}
  }
}
```

修改完之后，在 Caddyfile 所在目录运行`caddy reload`就可以重新加载配置了

# 反向代理增加 Basic Auth

第一步需要 hash 一下密码，caddy 不希望我们写明文密码，比如我们的密码是 123456

```bash
$ caddy hash-password --plaintext 123456
$2a$14$ZTwlgDTKk38.53Z0QhkuJ.iwmOwnK1ggYs2O8M6eT0ivTwTeVXxVS
```

修改配置文件 Caddyfile
后面我们请求的时候，就会需要先输入用户名密码才能访问服务

```groovy
http://example.com:8080 {
    basicauth / {
        # user: rainbow, password: 123456
	    rainbow $2a$14$ZTwlgDTKk38.53Z0QhkuJ.iwmOwnK1ggYs2O8M6eT0ivTwTeVXxVS
	}
	reverse_proxy localhost:8080
}
```

# 安装

DEB 安装

```bash
wget https://github.com/caddyserver/caddy/releases/download/v2.6.4/caddy_2.6.4_linux_amd64.deb
sudo dpkg -i caddy_2.6.4_linux_amd64.deb

# 控制命令
systemctl restart caddy
systemctl reload caddy

# 修改配置文件
vi /etc/caddy/Caddyfile
```
