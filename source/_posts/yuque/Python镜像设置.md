---
title: Python镜像设置
urlname: sgda05691v8sevc3
date: '2023-04-23 11:08:56 +0800'
tags: []
categories: []
toc: true
---

# 使用一些知名的镜像

```bash
# 目前使用下来发现ustc是国内镜像最快的
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
pip config set global.extra-index-url https://pypi.org/simple
```

一些工具可以自动找到最快的 pypi 镜像，比如 [https://pypi.org/project/faster/](https://pypi.org/project/faster/)

其他一些可用的镜像

- 清华大学 [https://pypi.tuna.tsinghua.edu.cn/simple](https://pypi.tuna.tsinghua.edu.cn/simple)
- 豆瓣 [https://pypi.doubanio.com/simple](https://pypi.doubanio.com/simple)
- 华中科技大 [https://mirrors.ustc.edu.cn/pypi/web/simple](https://mirrors.ustc.edu.cn/pypi/web/simple)

# 自建镜像缓存

使用外部镜像的好处是方便，不过也有两个问题

1. 官方镜像也会出问题，我就遇到过 douban 镜像不行了，阿里云镜像限速
2. 官方镜像往往获取不到最新上传的包

所以自建一个 pypi 的镜像代理就很有必要，经过一番搜索找到了[proxpi](https://github.com/EpicWink/proxpi)这个项目
安装和使用方法都非常简单

```bash
# 安装
pip install proxpi

# 配置INDEX缓存时间
export PROXPI_INDEX_TTL=60
# 配置最长等待下载时间，超时就302重定向到mirror的镜像地址
export PROXPI_DOWNLOAD_TIMEOUT=300
# 配置二级镜像
export PROXPI_EXTRA_INDEX_URLS=https://pypi.tuna.tsinghua.edu.cn/simple
# 配置二级镜像TTL, 默认3分钟，这里调成30s
export PROXPI_EXTRA_INDEX_TTLS=30
# 配置缓存文件夹
export PROXPI_CACHE_DIR=$PWD/pypi
# PROXPI_CACHE_SIZE=5000000000 默认5G，这个可以不用改

# 强制contentType为application/octet-stream
# 这个必须要加，不然poetry会把tar.gz认为是tar文件，导致hash错误
PROXPI_BINARY_FILE_MIME_TYPE=1

# 启动服务
FLASK_APP=proxpi.server flask run --port 31415
```

本地 Python 配置，这里假设 proxpi 的 server 地址是 10.0.0.1:31415

```bash
# 跟通常的不太一样，它这个不是/simple而是/index
pip config set global.index-url http://10.0.0.1:31415/index
pip config set global.trusted-host 10.0.0.1:31415

# 下载个大的文件试试
pip install opencv-python

# 或者不通过配置，直接命令行指定
pip install -i http://10.0.0.1:31415/index --trusted-host 10.0.0.1:31415 opencv-python
```
