---
title: NodeJS安装和镜像配置
urlname: rvmf4lg0a0fgf4to
date: '2023-05-04 19:56:45 +0800'
tags: []
categories: []
toc: true
---

这个方法适用于 Linux，通过运行命令可以快速的装上 nodejs

```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.3/install.sh | bash
. ~/.bashrc
nvm install 16
```

更换淘宝镜像

```python
npm config set registry https://registry.npm.taobao.org
```

## 参考

- [https://github.com/nvm-sh/nvm](https://github.com/nvm-sh/nvm)
