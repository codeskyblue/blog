---
title: 网络同步盘Syncthing介绍
urlname: kant5kwuz055mr4a
date: '2023-07-20 10:40:59 +0800'
tags: []
categories: []
toc: true
---

# 背景

在现在网盘到处限速的情况下，而且还时不时的删资源，搞不好还能关停（@360 云盘），最重要的还是隐私问题，你把数据交给云盘，它就真的不会看看里面是啥内容吗？
之前尝试过 Nextcloud，可惜这个体验总感觉差这么一点，它用的是传递的用户名密码方案，总感觉安全差点意思。
功夫不负有心人，最近发现了一个工具 Syncthing，这个工具非常的优秀
Syncthing 有很多的优点

1. 同步速度快，支持文件系统监听，一有修改立刻同步，并且速度可以直接打满带宽。
2. 数据加密传输，传输数据前需要各个节点确认，安全性很高
3. 分布式技术，支持部分节点故障的情况下，剩余节点正常同步
4. 支持文件版本管理，找回误删除的数据
5. 支持配置忽略模式，不想同步的文件不同步
6. 部署方便，因为是用 Go 编写的，只有一个二进制，并支持的多个平台部分（Windows，Linux，Mac，Android）

不过也有一些缺点

1. 当对一个文件夹重命名时，同步端会先把原文件夹删除再下载新重命名的文件夹，效率有点慢
2. iPhone 没有对应的免费客户端
3. 同步使用 NAS 下 SMB 挂载的目录时，如果直接通过 NAS 添加文件，syncthing 会感知不到文件变化就不同步了。另外也没有带同步端没有强制同步的按钮，不能手动同步。

# 使用

下面就介绍一下下面的这个使用场景怎么部署。
小明在家中有一台华为家庭存储，一台在家中长期运行的 Linux 主机，并且还有一台 Mac 笔记本电脑。
他有两个使用场景

1. Mac 修改的内容能够随时备份到家中的家庭存储中，并且当误删除文件的时候，能通过家庭存储找回数据。
2. 将家庭存储的部分资源（如通过迅雷下载的电影）同步到 Mac 中

## 华为家庭存储设置

华为 NAS 先开启 SMB，设置用户名密码，这里假设用户名 kitty 密码 12345 家庭存储的 IP 是**192.168.1.2**
![](/images/yuque/FoFDI7_u7CFr1LLNyeJxgW5IYsmH.png)

## Linux 主机设置

这里我假设你是通过你的 Mac 电脑通过 SSH 远程访问的 Linux 主机，毕竟长期运行的 Linux 一般也用不着屏幕。

1. 使用 Mount 命令挂载 SMB 到本地的一个目录

```bash
$ sudo mount -t cifs -o rw,file_mode=0644,dir_mode=0755,username=kitty //192.168.1.2/<这里换成华为用户名> ~/MyNAS
# 提示输入密码的时候输入密码
```

2. 在~/MyNAS 下面创建一个叫 Sync 的目录
3. 从[https://syncthing.net/](https://syncthing.net/)网站上将 Linux 版本的 syncthing 下载下来，二进制复制到/usr/local/bin
4. 直接运行`./syncthing`
5. Syncthing 会默认监听本地的 8384 端口，这里使用 ssh 命令将这个服务转发到 Mac 上来

```bash
$ ssh -L 18384:localhost:8384 用户名@Linux的IP
```

然后就可以在电脑上的[http://localhost:18384](http://localhost:18384)访问 syncthing 的控制界面了。
![](/images/yuque/FuXHwnZNdCaKOnYZvGmkkktQpRzS.png)

6. 不过这里的 Default Folder 对应的目录还是 ~/Sync, 我们先直接将这个移除掉，改成保存路径~/MyNAS/Sync

点击![](/images/yuque/Fk6q1Dl1w6bto2b0_AqrYb9Dl3vO.png)
然后按照下面的截图中这样写就行了，注意文件夹 ID 最好写成 default，不然跟其他设备同步的时候会麻烦一点。
![](/images/yuque/FutRMmuLt32KpIerhcNXoi5Cc8SW.png)

7. 因为 Syncthing 对于 NAS 通过 SMB 挂载的文件监听不敏感，所以将扫描间隔从 3600s 调整为 60s

![](/images/yuque/Fo0B2W6qKHG16hn-hQ747fe1bBMb.png)

## Mac 电脑配置

1. 从[https://syncthing.net/](https://syncthing.net/)网站上将 Mac 版的 dmg 文件，直接安装就可以了。安装完成后会在顶部的状态栏出现一个小图标。
2. 点击设置，勾选一下开机启动
   ![](/images/yuque/FkW5Y7hU9mlsnyU31_d6kN4TOV8Q.png)
3. 本地浏览器打开[http://localhost:8384](http://localhost:8384)，点击右下角的添加远程设备
   ![](/images/yuque/FgOpMmqeAhSzIRP7bhHbjd-tokQE.png)
4.
