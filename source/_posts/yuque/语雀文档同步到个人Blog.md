---
title: 语雀文档同步到个人Blog
urlname: any1s4wcvpwonlsa
date: '2023-04-18 23:02:46 +0800'
tags:
  - 语雀
categories: []
---

# 背景

之前我也曾搞过个人 blog，体验过很多，比如 hugo，hexo，oschina 上的 blog，testerhome 博客，知乎个人空间。但是都有点不太满意其中的编写阶段。要么是需要用编辑器写 markdown，要么就是得登录网站写，像知乎发个文章还得审核。自从见到了[yuque-hexo](https://github.com/x-cold/yuque-hexo)项目，我才有点感觉自己这个 blog 的春天来了。语雀用起来的体验是我用过的所有编辑器里面体验最好的，既可以网页修改，也可以装客户端（手机、PC 都有），最关键的时候还支持 markdown。通过 yuque-hexo 项目能快速的将语雀的文档导入到 hexo 项目中，然后直接生成 html 静态网站，简直不能再方便。下面就讲讲我是如何配置的。

> 不过也有不好的一点，就是快要收费了，价格还不低。希望语雀能够认清现实，不然我就跑了。

# 教程

因为改了很多东西，为了方便，可以直接[fork 我的项目 codeskyblue/hexo-blog-template](https://github.com/codeskyblue/hexo-blog-template/fork)
Fork 完之后，git clone 到本地

1. 修改配置文件 `_config.yml`中的 title, author, url 字段，改成自己的
2. 将 source 目录直接删掉（不用担心，yuque 同步的时候还会自动创建）

## 获取 YUQUE_TOKEN

![](/images/Frc9TbxcBhlaeQHma7FmvLOdLZ9Y.png)
然后点击下面的 Token 就能获取了
![](/images/Fux9lAfHUTXLc1XQUm1G4AO7G6Ou.png)

> 看起来还需要超级会员（目前看到的价格是 299/年）还不便宜，因为以前创建过所有就直接用以前创建的

获取完 TOKEN 之后，将其设置环境变量

```bash
# Linux
export YUQUE_TOKEN=xxxx

# Windows
set YUQUE_TOKEN=xxxx
```

## 获取语雀账户名和知识库地址

下面两个是要修改的东西 （文件路径 package.json)
![](/images/FpNw6b4nrhfc--TIWmBA0mWoR6JV.png)
直接点击这里
![](/images/FnhxsvXwrm2KzS2r5hCnDzZ-4tpp.png)
直接进入你要看的知识库，然后其中的 URL 就是要提取的信息
比如我的 [https://www.yuque.com/codeskyblue/blog](https://www.yuque.com/codeskyblue/blog)
其中 login 是 codeskyblue，repo 是 blog

## 同步 yuque 的内容到本地

```bash
export YUQUE_TOKEN=xxxx
npm run sync
```

看一下控制台输出，如果有报错，根据报错在谷歌百度或者[chatgpt](https://chat.codeskyblue.xyz)一下。

接下来可以预览一下效果了（命令运行完后会自动打开一个网站）

```bash
npm run server
```

# 项目部署到个人网站

有很多中办法，最简单的就是 npm run generate 生成的 public 目录直接 copy 到静态网站上去
我目前是 digitalocean 上建了一个静态网站，关联了 Github 项目，直接一 push 就会自动部署。这个应该比较简单了，具体步骤就不写了。

我目前的博客地址 [https://blog.codeskyblue.xyz](https://blog.codeskyblue.xyz) 欢迎常来看看

---

后面的内容就可以不看了，都是我没有试验通过的。感兴趣的可以看别的博主的实践。

# 通过语雀 webhook 自动更新 blog(未完）

未完估计不待续了

## 创建 github token

创建新的 Github Token [https://github.com/settings/tokens/new](https://github.com/settings/tokens/new)
![](/images/FuHmcy1LtNsX_ydNAM9ttfwNVUJ-.png)

另外项目的 Workflow 的权限也要赋予一下，不然不能自动 Commit And Push
![](/images/FhODs8YgBhM-crA9Wsg6PVMpupTw.png)

# 遗留问题

1. 语雀的 webhook 好像没用
2. github 的 action 插件 Git commit and push，也没看到 push
3. 腾讯[COS](https://console.cloud.tencent.com/cos/bucket)配置（看起来还需要备案，懒得搞了）
