---
title: Python AES加解密
urlname: nwhp7gt5ai7ugnzc
date: '2023-09-21 19:00:53 +0800'
tags: []
categories: []
toc: true
---

# 简介

高级加密标准（Advanced Encryption Standard: AES）是美国国家标准与技术研究院（NIST）在 2001 年建立了电子数据的加密规范。其是对称加解密算法的最经典算法之一，它是一种分组加密标准，每个加密块大小为 128 位，允许的密钥长度为 128、192 和 256 位。这里只介绍 ECB 加密模式。
AES 加密模式：ECB/CBC/CTR/OFB/CFB
填充：pkcs5padding/pkcs7padding/zeropadding/iso10126/ansix923
数据块：128 位/192 位/256 位

# 使用

安装依赖

```bash
# For Linux and Darwin
pip install pycrypto

# For windows
pip install pycryptodome
```

比较遗憾的是，Python 的 PKCS5 的实现需要自己来，虽然也不是太难。不过有点麻烦
具体实现

```python
from Crypto.Cipher import AES

def pad(s: str) -> str:
    """ padding PKCS5 """
    block_size = AES.block_size # always 16
    return s + (block_size - len(s) % block_size) * chr(block_size - len(s) % block_size)


def unpad(s: bytes) -> str:
    """ Unpadding PKCS5 """
    return s[:s[-1]].decode('utf-8')


def encrypt(s: str, password: bytes) -> bytes:
    cipher = AES.new(password, AES.MODE_ECB)
    return cipher.encrypt(pad(s).encode('utf-8'))


def decrypt(hex_string: str, password: bytes) -> str:
    raw = bytearray.fromhex(hex_string)
    cipher = AES.new(password, AES.MODE_ECB)
    pad_string = cipher.decrypt(raw)
    return unpad(pad_string)


if __name__ == "__main__":
    password = b"1234567890123456"
    v = encrypt("Hello world", password)
    secret_message = v.hex()

	message = decrypt(secret_message, password)
    print("Message is", message)
```

# 参考链接

https://juejin.cn/post/7026635907742564365
