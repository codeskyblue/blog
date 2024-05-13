---
title: Linux虚拟内存创建
urlname: uny9xkvq36xilz9x
date: '2023-06-05 16:51:29 +0800'
tags: []
categories: []
toc: true
---

写了一个脚本方便一键扩容虚拟分区
简单版本

```bash
swapoff -a
dd if=/dev/zero of=/swapfile bs=1M count=2000
chmod 600 /swapfile
mkswap /swapfile
swapon /swapfile
grep SwapTotal /proc/meminfo
```

复杂版本

```bash
#!/bin/bash
#

if test $(whoami) != root
then
	echo "require root privilege"
	exit 1
fi

SWAPFILE_SIZE_GB=8 # 8GB

SWAPFILE_SIZE=$(stat --format="%s" /swapfile)
EXPECT_SIZE=$(($SWAPFILE_SIZE_GB << 30))
if [[ $SWAPFILE_SIZE == $EXPECT_SIZE ]]
then
	echo "Swapfile is no need to expand."
	exit 0
fi

swapoff -a
dd if=/dev/zero of=/swapfile bs=1G count=${SWAPFILE_SIZE_GB:-8}
chmod 600 /swapfile
mkswap /swapfile
swapon /swapfile
grep SwapTotal /proc/meminfo

```
