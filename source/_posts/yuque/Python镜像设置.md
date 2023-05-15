---
title: Python镜像设置
urlname: sgda05691v8sevc3
date: '2023-04-23 11:08:56 +0800'
tags: []
categories: []
toc: true
---

```bash
# 目前使用下来发现ustc是国内镜像最快的
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
```

一些工具可以自动找到最快的 pypi 镜像，比如 [https://pypi.org/project/faster/](https://pypi.org/project/faster/)

其他一些可用的镜像

- 清华大学 [https://pypi.tuna.tsinghua.edu.cn/simple](https://pypi.tuna.tsinghua.edu.cn/simple)
- 豆瓣 https://pypi.doubanio.com/simple
- 华中科技大 [https://mirrors.ustc.edu.cn/pypi/web/simple](https://mirrors.ustc.edu.cn/pypi/web/simple)
