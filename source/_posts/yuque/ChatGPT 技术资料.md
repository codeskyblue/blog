---
title: ChatGPT 技术资料
urlname: pbxc0ygvvo7la13h
date: '2023-05-05 09:47:38 +0800'
tags: []
categories: []
toc: true
---

# 模型

## 参考

- [https://platform.openai.com/docs/models/overview](https://platform.openai.com/docs/models/overview)

# 限流

**RPM：request per minute**
**TPM: tokens per miniute**
**gpt-4**/**gpt-4-0314** are 40k TPM and 200 RPM
**gpt-4-32k**/**gpt-4-32k-0314** are 80k TPM and 400 RPM
参考 [https://platform.openai.com/docs/guides/rate-limits/overview](https://platform.openai.com/docs/guides/rate-limits/overview)

代码参考
[https://github.com/openai/openai-cookbook](https://github.com/openai/openai-cookbook) 这个项目提供了非常多的例子，如 token 计算，限流，怎么用 flask 写的给小狗起名的例子
[https://github.com/openai/openai-quickstart-python](https://github.com/openai/openai-quickstart-python)

# Playground

用来做一些快速的测试比较方便
[https://platform.openai.com/playground](https://platform.openai.com/playground)

# 常见错误

```bash
# 使用免费账号的时候出现
openai.error.RateLimitError: You exceeded your current quota, please check your plan and billing details.

```

#
