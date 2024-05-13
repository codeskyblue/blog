---
title: 将Github上的Python项目发布到PYPI
urlname: pm1hiotl8isy03r7
date: '2023-05-04 15:55:39 +0800'
draft: true
tags: []
categories: []
toc: true
---

以下都是我实践过的步骤，内容包含

- 如何使用 poetry 创建项目
- 从 git 的 tag 中获取版本号
- 配置 Github Actions
  - 配置单元测试上传到 codecov.io
  - 配置 tag push 自动触发 publish
  - 更新 README 中的 badge

<!-- more -->

# Poetry

poetry 可以代替目前的 setup.py 和 requirements.txt 组合，虽然部分命令跑起来有点慢，但是胜在方便
下面这个文件是可以通过命令`poetry init`命令生成的，不用复制粘贴。

```toml
[tool.poetry]
name = "sshg"
version = "0.1.0"
description = "ssh from config with arrow select support"
authors = ["codeskyblue <codeskyblue@gmail.com>"]
license = "MIT"
readme = "README.md"

[tool.poetry.dependencies]
python = "^3.8"
Jinja2 = "^3.1.2"
requests = "*"
dataclasses-json = "*"
pyyaml = "*"
prompt_toolkit = "*"
pexpect = "*"

[tool.poetry.dev-dependencies]
pytest = "^7.2.0"
pytest-cov = "^2"

# 需要自定义脚本命令的话再设置
[tool.poetry.scripts]
sshg = "sshg:main"

# 根据tag来动态配置版本号
[tool.poetry-dynamic-versioning]
enable = true

[build-system]
requires = ["poetry-core>=1.0.0", "poetry-dynamic-versioning"]
build-backend = "poetry_dynamic_versioning.backend"
```

如果是通过交互式命令创建出来的 pyproject.toml 需要再添加点内容，其中 build-system 部分需要替换掉

```toml
# 需要自定义脚本命令的话再设置
[tool.poetry.scripts]
sshg = "sshg:main"

# 根据tag来动态配置版本号,tag需要v开头，比如v0.0.1
[tool.poetry-dynamic-versioning]
enable = true

# 需要将原本的build-system替换掉
[build-system]
requires = ["poetry-core>=1.0.0", "poetry-dynamic-versioning"]
build-backend = "poetry_dynamic_versioning.backend"
```

下面是一些常用命令

```bash
# 更新poetry.lock文件
poetry update

# 安装到poetry的虚拟环境（每个项目一个单独的虚拟环境）
poetry install

# 进入poetry 虚拟环境
poetry shell

# 编译tar.gz和whl包
poetry build
```

## 参考

- [https://python-poetry.org/docs/](https://python-poetry.org/docs/) poetry 的官网
- [https://github.com/python-poetry/poetry](https://python-poetry.org/docs/) poetry 的源码网站
- [https://github.com/mtkennerly/poetry-dynamic-versioning](https://github.com/mtkennerly/poetry-dynamic-versioning)

# Github Actions

## 创建配置文件

参考配置文件，根据需要修改，下面的文件直接复制到路径`.github/workflows/python-app.yml`
下面的命令可以方便的完成

```bash
mkdir -p .github/workflows
cat > .github/workflows/python-app.yml
```

下面的内容是要贴过去的内容

```yaml
name: Python Package

on:
  push:
    branches: [master]
    tags:
      - v*
  pull_request:
    branches: [master]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - name: Set up Python 3.9
        uses: actions/setup-python@v2
        with:
          python-version: 3.9

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install poetry
          poetry install

      - name: Run tests with coverage
        run: |
          poetry run pytest --cov=. --cov-report xml --cov-report term

      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v3

  publish:
    runs-on: ubuntu-latest
    needs: test # 声明依赖于先前的测试作业
    if: startsWith(github.ref, 'refs/tags/') # 仅在标签推送时运行
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: 3.9

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install poetry

      - name: Build
        run: |
          poetry self add "poetry-dynamic-versioning[plugin]"
          rm -fr dist/ && poetry build

      - name: Publish distribution 📦 to PyPI
        uses: pypa/gh-action-pypi-publish@release/v1
        with:
          password: ${{ secrets.PYPI_TOKEN }}
```

正常的话可以看到 github 的 actions 被正常触发
![](/images/yuque/FpJbmq2bai7LXA8TsKXNoWAYurEK.png)

配置文件可以本地先测试一下，使用这个项目 [https://github.com/nektos/act](https://github.com/nektos/act)
运行命令 `act --list`就可以检查语法是否正常了。

## 配置 PYPI_TOKEN

先要拿到 token
[https://pypi.org/manage/account/token/](https://pypi.org/manage/account/token/)
然后生成的 token 添加到项目的 Repository secrets 中去，下面用图来说明一下
![](/images/yuque/Fok0U6cFEi21YOx2dCwYh366P0Bo.png)
Name 就写`PYPI_TOKEN`，Secret 就把刚才生成的 token 帖进去
![](/images/yuque/FsTklGo2sSU0AsltR5qH0z0F7sI8.png)

# Coverage

[https://codecov.io/](https://codecov.io/) 也需要设置一下变量 CODECOV_TOKEN，进入到指定项目中会有指引，这里就不写了。另外 badge 也可以从网站上直接 Copy 下来。
pyproject.toml 中新增下面的内容

```toml
[tool.coverage.run]
branch = true

[tool.coverage.report]
# Regexes for lines to exclude from consideration
exclude_also = [
    # Don't complain about missing debug-only code:
    "def __repr__",
    "if self\\.debug",

    # Don't complain if tests don't hit defensive assertion code:
    "raise AssertionError",
    "raise NotImplementedError",

    # Don't complain if non-runnable code isn't run:
    "if 0:",
    "if __name__ == .__main__.:",

    # Don't complain about abstract methods, they aren't run:
    "@(abc\\.)?abstractmethod",
    ]

ignore_errors = true
omit = [
    "tests/*",
    "docs/*"
]
```

文件文件 coveragerc

```toml
[run]
branch = true

[report]
# Regexes for lines to exclude from consideration
exclude_also =
    # Don't complain about missing debug-only code:
    "def __repr__",
    "if self\\.debug",

    # Don't complain if tests don't hit defensive assertion code:
    "raise AssertionError",
    "raise NotImplementedError",

    # Don't complain if non-runnable code isn't run:
    "if 0:",
    "if __name__ == .__main__.:",

    # Don't complain about abstract methods, they aren't run:
    "@(abc\\.)?abstractmethod",

ignore_errors = true
omit =
    "tests/*",
    "docs/*"
```

有时候需要忽略部分含，可以通过注释来实现

```python
a = my_function1()
if debug:  # pragma: no cover
    msg = "blah blah"
    log_message(msg, a)
b = my_function2()
```

参考：[https://coverage.readthedocs.io/en/latest/config.html](https://coverage.readthedocs.io/en/latest/config.html)

# Badge

这是个好东西，可以直接展示覆盖率，最新版本号之类的东东
比如
![](/images/yuque/Fp7tEetijw_XVg5hof4lR72ysY3o.png)
[https://badge.fury.io/for/py](https://badge.fury.io/for/py)
通过这个网站就可以快速生成你需要的 badge，使用体验很好

## 参考

- [https://codecov.io](https://codecov.io)
- [https://badge.fury.io/](https://badge.fury.io/)
