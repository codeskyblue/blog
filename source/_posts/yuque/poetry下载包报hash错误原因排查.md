---
title: poetry下载包报hash错误原因排查
urlname: souq08lf43izvfcr
date: '2023-11-22 16:55:22 +0800'
tags: []
categories: []
toc: true
---

# 问题

执行 poetry install 的时候出现 sha256 校验失败
![](/images/yuque/FkcZ81v9VmKfiOwHrI5zBCii5DkE.png)

# 排查

## 猜测 1：是不是 pypi 源出问题了

因为我用的是自建的 pypi 代理，[https://github.com/EpicWink/proxpi/](https://github.com/EpicWink/proxpi/tree/master) 能将包缓存到本地，提高下载速度。
先换掉本地代理，直接走官方源 pypi.org 试试，哎，正常了。
可是官方源慢啊，必须得走 pypi 代理呀，所以一定要找出来 pypi 代理出啥问题了

## 猜测 2： 难道是 pypi 上的包不对？

直接去代理的地址找到对应

```bash
$ find . | grep colored | xargs sha256sum
04ff4d4dd514274fe3b99a21bb52fb96f2688c01e93fba7bef37221e7cb56ce0  ./pypi/files-pythonhosted-org/packages/f3/d6/00203998f27ab30b2417998006ad0608f236740bb129494dd7c5621861e1/colored-1.4.4.tar.gz
```

看 hash 值也没问题，跟 pypi.org 上的一样
![](/images/yuque/FhA9MWBH-fwyg7cIZPpK2wO9s-ZO.png)

## 猜测 3：说不定是 poetry 的本地缓存出问题了

先是调用了一下 poetry 自己的命令，清空自身缓存

```bash
$ poetry cache clear . --all
$ poetry install
```

没效果。还是报一样的错误

## 猜测 4：说不定代理没有读本地文件，直接读的内存

先重启一下代理服务，下包试试

```bash
$ wget -q https://pypiproxy.example.com/index/colored/colored-1.4.4.tar.gz -O- | shasum -a256
04ff4d4dd514274fe3b99a21bb52fb96f2688c01e93fba7bef37221e7cb56ce0
```

看起来没什么问题，hash 正确。
再试试 poetry 清缓存，然后 install，依然报错。

## 猜测 5：poetry 莫非还有没清的缓存

直接翻源码，一路找到代码下载的位置
[https://github.com/python-poetry/poetry/blob/2b50120c86ae72781357411342f2feda0a4e2713/src/poetry/utils/helpers.py#L141](https://github.com/python-poetry/poetry/blob/2b50120c86ae72781357411342f2feda0a4e2713/src/poetry/utils/helpers.py#L141)
![](/images/yuque/Fp6JkPXkzfVM5b54By04h5-cEZCL.png)
增加一行

```python
print("Download", url, dest)
```

最后发现，确实下载了。但就是下载的文件 sha 值不对。
解压包试试呢 tar -xzvf colored-1.4.4.tar.gz，简单的看了一下，内容是对的。没什么问题。

## 猜测 6：难道是 requests 出问题了

这个想法我自己都觉的离谱，requests 怎么可能出问题
让 GPT 写一个通过 requests 下载代码并校验 sha256 的功能看看, GPT 效率非常的高，很快就写好了

```python
import requests
import hashlib

url = "https://pypiproxy.example.com/index/colored/colored-1.4.4.tar.gz"
filename = "colored-1.4.4.tar.gz"

r = requests.get(url, stream=True)

if r.status_code == 200:
    with open(filename, "wb") as f:
        for chunk in r.iter_content(chunk_size=1024):
            f.write(chunk)

    print(f"File '{filename}' downloaded successfully.")

    # Calculate SHA256 hash
    sha256_hash = hashlib.sha256(open(filename, "rb").read()).hexdigest()
    print(f"SHA256 hash: {sha256_hash}")
else:
    print("Failed to download the file.")
```

执行后输出什么呢

```bash
$ python download.py
File 'colored-1.4.4.tar.gz' downloaded successfully.
SHA256 Hash of the downloaded file: b7b48b9f40e8a65bbb54813d5d79dd008dc8b8c5638d5bbfd30fc5a82e6def7a
```

看来 requests 有问题，可为什么文件是一样的呢？太奇怪了。
让 GPT 重写一下代码，将 requests 替换为 urllib 下载。
没想到下载到的文件 hash 竟然又对了。看来问题就出在 requests 上，但是就是不知道为什么。问 GPT4 也没给出什么有用的答案。
既然如此，代理上的那个 colored-1.4.4.tar.gz 文件，直接改成 hello 文本。我倒要看看 requests 怎么整出来不同的文件 hash

```bash
echo hello > colored-1.4.4.tar.gz
```

视角转到自己的电脑上，执行命令，出现了。下载报错

```bash
$ python download.py
requests.exceptions.ContentDecodingError: ('Received response with content-encoding: gzip, but failed to decode it.', error('Error -3 while decompressing data: incorrect header check'))
```

到这里终于看到了成功的曙光了。问题原因出在 requests 下载的时候会自己 decode 呀。
之前下载的那个 colored-1.4.4.tar.gz 用 file 命令看看

```bash
$ file colored-1.4.4.tar.gz
colored-1.4.4.tar.gz: POSIX tar archive (GNU)
```

我擦，果然是 tar 文件。破案了，原来是，requests 直接帮忙把 tar.gz 解压了成 tar 文件了，但是文件名没改。难怪外表看起来一样，但是 hash 一直不对。

## 结论

requests 库下载文件的时候，会自动把 tar.gz 解压了成 tar 文件了，导致 hash 一直不对。更换 urllib 获取直接 curl 请求的下载就是正确的。

# 问题修复

## 修复方案 1

既然是 requests 自动解压了，那就想办法把 Content-Encoding: gzip 从服务端先去掉吧。让 requests 不自动解压。
查看了一下我那个代理的源码文档。有一个配置看起来可以。
![](/images/yuque/FsdK4k-XIpjwp0_8DFxLMXGZSqdC.png)
再看 flask 的源码，发现只要设置了 mimetype，Content-Encoding 就不会设置。
![](/images/yuque/FsAlDcy0_636fUJrLZlCLGgB2IvL.png)
修改完之后，重启 proxi 代理测试一下

```bash
$ http HEAD https://pypiproxy.example.com/index/colored/colored-1.4.4.tar.gz
HTTP/1.1 200 OK
Cache-Control: no-cache
Connection: keep-alive
Content-Disposition: inline; filename=colored-1.4.4.tar.gz
Content-Length: 36786
Content-Type: application/octet-stream
Date: Thu, 23 Nov 2023 03:05:09 GMT
ETag: "1700647547.9076493-36786-988557199"
Last-Modified: Wed, 22 Nov 2023 10:05:47 GMT
Server: gunicorn
Strict-Transport-Security: max-age=31536000
X-protocol: HTTP/1.1
```

这里看到 Content-Encoding 不见了。
再次测试一下 poetry，先清缓存再 poetry install。终于不报错误了。完美

## 修复方案 2

改一下 poetry，让其使用 requests 下载的时候不再自动解码

```python
# Ref: https://stackoverflow.com/questions/18364193/requests-disable-auto-decoding
import requests

url = https://pypiproxy.example.com/index/colored/colored-1.4.4.tar.gz
r = requests.get(url, stream=True)
with open(local_filename, 'wb') as f:
    for chunk in r.raw.stream(1024, decode_content=False):
        if chunk:
            f.write(chunk)
```

相关 issue
[https://github.com/python-poetry/poetry/issues/4523](https://github.com/python-poetry/poetry/issues/4523)
