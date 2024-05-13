---
title: POC：使用ChatGPT多模态实现App登录
urlname: grhu3465pgigc6na
date: '2024-05-13 14:27:38 +0800'
tags: []
categories: []
toc: true
---

## App 登录

为了限制一下模型的操作，我们把可能的区域用数字做了标记区分。
![](/images/yuque/Ft47ZEpiwk1dCYNT0OdDYg4zRFbx.png)

```bash
>> Question with Image
You are given the Android screenshot. I need to input the (username or phone number) in order to complete the login step. The possible tap positions are marked as numbers with red color. You need to choose the right number to tap and input.

>> Answer
Based on the screenshot you provided, it looks like the numbers are indicating potential tap points. For entering a username or phone number to log in, you would want to tap where the input field is. In the screenshot, it appears that the input field for the phone number or username is located next to "+86" with a placeholder text that likely suggests entering the phone number.

From your description, the correct number to tap to input the username or phone number is marked with the number 4 in red color. Tap on this number to bring up the keyboard and enter your details.

>> Question
I need to input a password. Can you provide guidance on which number positions I should tap?

>> Answer
For entering the password, the correct tap position based on the screenshot you provided earlier would be where the placeholder text indicating the password field is located. In your screenshot, this placeholder for the password is marked with the number 5 in red. So, you should tap on number 5 to enter your password.

>> Question
Now I need to click login button. output the number which should tap

>> Answer
Based on the layout of the login screen in the screenshot you provided, the login button is located at the bottom of the screen in a yellow rectangular button. From the description of the numbers marked in red, the login button is marked with the number 7. Therefore, you should tap on number 7 to proceed with logging in.
```

当我询问如何输入用户名的时候，GPT 给出了正确的位置 4，而需要输入密码的时候，GPT 给出的正确的位置 5.
这个有两个关键点

1. 标记处图片中可以点击的点
2. 使用恰当的 Prompt 来让 GPT 输出正确的结果。

当前 Activity：com.meituan.passport.LoginActivity
根据 GPT 给出的内容生成脚本

- Tap //\*[@resource-id="com.sankuai.meituan:id/passport_mobile_phone"]
- Input 电话号码
- Tap //\*[@resource-id="com.sankuai.meituan:id/edit_password"]
- Input 密码
- Tap //\*[@resource-id="com.sankuai.meituan:id/login_button"]
