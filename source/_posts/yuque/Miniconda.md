---
title: Miniconda
urlname: ceypuxsfc9hpgwu0
date: '2023-05-11 16:32:23 +0800'
tags: []
categories: []
toc: true
---

## 简介

miniconda 是一款小巧的 python 环境管理工具，安装包 50 多 MB，它能够创建独立的 Python 虚拟环境，并支持特定的 Python 版本创建。并且支持在各种平台安装。
大约相当于 virtualenv + pyenv

## 安装

直接去官网下载对应的文件 [https://docs.conda.io/en/latest/miniconda.html](https://docs.conda.io/en/latest/miniconda.html)
比如我的电脑是 Mac X86 芯片的

```bash
# I like python 3.9
wget https://repo.anaconda.com/miniconda/Miniconda3-py39_23.3.1-0-Linux-x86_64.sh

# -b           run install in batch mode (without manual intervention),
# it is expected the license terms (if any) are agreed upon
# -f           no error if install prefix already exists
# -h           print this help message and exit
# -p PREFIX    install prefix, defaults to /home/ubuntu/miniconda3, must not contain spaces.
# -s           skip running pre/post-link/install scripts
# -u           update an existing installation
# -t           run package tests after installation (may install conda-build)
bash Miniconda3-py39_23.3.1-0-Linux-x86_64.sh -b
```

这个 sh 脚本大的很，既有可读脚本，又附加有二进制
默认安装到 ~/miniconda3 目录，想换别的路径使用-p 指定，比如`-p /opt/miniconda3`

conda 安装完之后，会默认在当前 shell 的 rc 配置文件中写入 conda 的初始化脚本，并启用 conda 的 base 环境。这样你运行 python 的时候，默认就变成了 conda 的 python。如果希望默认不启用的话，就执行下面的命令

```
# 默认不开启base环境（可选）
# 影响~/.condarc文件
conda config --set auto_activate_base false
```

## 设置软件源

由于 conda 在国外(M 国), 软件速度不是这么快。可以通过设置软件源来加速

```
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
conda config --set show_channel_urls yes
```

## 使用

下面试试创建一个虚拟环境试试，环境名就叫 foo

```
conda create -n foo python=3.5
# 激活环境
conda activate foo
# 检查python版本
python -V
# 使用pip安装一个库
pip install requests
# 离开当前环境
conda deactivate foo
```

# Docker 上如何安装

```
bash Miniconda3-latest-Linux-x86_64.sh -b
$HOME/miniconda3/bin/conda create python=3.7 -n modelscope -y
```

## 参考文档

- Docker 镜像地址 [https://hub.docker.com/u/continuumio](https://hub.docker.com/u/continuumio)
- 官网下载地址 [https://docs.conda.io/en/latest/miniconda.html](https://docs.conda.io/en/latest/miniconda.html)
- [https://zhuanlan.zhihu.com/p/133494097](https://zhuanlan.zhihu.com/p/133494097)
- Cheetsheet [https://kapeli.com/cheat_sheets/Conda.docset/Contents/Resources/Documents/index](https://kapeli.com/cheat_sheets/Conda.docset/Contents/Resources/Documents/index)
- Docker [https://stackoverflow.com/questions/58269375/how-to-install-packages-with-miniconda-in-dockerfile](https://stackoverflow.com/questions/58269375/how-to-install-packages-with-miniconda-in-dockerfile)
