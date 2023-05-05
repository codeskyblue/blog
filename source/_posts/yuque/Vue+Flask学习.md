---
title: Vue+Flask学习
urlname: csz72xtm9oheh4ky
date: '2023-05-05 20:32:30 +0800'
tags: []
categories: []
toc: true
---

# 创建项目

[https://cn.vuejs.org/guide/scaling-up/tooling.html](https://cn.vuejs.org/guide/scaling-up/tooling.html)

```bash
npm init vue@latest
```

建议增加的插件

- TypeScript
- Pina
- Router

创建玩之后，修改一下 vite.config.js

```typescript
// https://vitejs.dev/config/
export default defineConfig({
  // 指定一下输出目录，方便flask使用
  build: {
    outDir: "../static",
    emptyOutDir: true,
  },
  //...
});
```

Flask 需要加上两个路由

```python
from flask import send_from_directory

app = flask.Flask(__name__)

@app.route("/")
def index():
    return send_from_directory("static", "index.html")

@app.route("/<path:path>")
def static_file(path: str):
    return send_from_directory("static", path)
```

这样子访问 Index 主页就可以直接加载 vue 编译出来的文件了

# 常用链接

- [https://cn.vuejs.org/](https://cn.vuejs.org/)
- ElementPlus [https://element-plus.org/zh-CN/component/button.html](https://element-plus.org/zh-CN/component/button.html)
- [https://vitejs.dev/config/](https://vitejs.dev/config/)
