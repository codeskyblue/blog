---
title: Android 投屏技术
urlname: oi4lyvaoy1dyqb9g
date: '2023-07-20 18:31:19 +0800'
tags: []
categories: []
toc: true
---

# 命令行

利用 screenrecord 和 ffmpeg 投屏

```bash
adb exec-out screenrecord --output-format h264 --size 640x310 - | ffmpeg -i - -f sdl -
```

可以根据选择自由调整屏幕
![](/images/yuque/Ftoh4QGkLggk9O-XOgGV08PR0gy5.png)

使用 Python PyAV 库解析

> PyAV 是 python 的 ffmpeg 绑定，并且提供 wheel 包，就算没装 ffmpeg 也能用

```python
import subprocess
import sys

import av


class Wrapper:
    """
    Wrapper which only exposes the `read` method to avoid PyAV
    trying to use `seek`.
    """

    name = "<wrapped>"

    def __init__(self, fh):
        self._fh = fh

    def read(self, buf_size):
        return self._fh.read(buf_size)


wrapper = Wrapper(sys.stdin.buffer)
with av.open(wrapper, "r") as container:
    for frame in container.decode():
        print(frame)
        pil_image = frame.to_image()
        pil_image.save("test.jpg")
        break
```

代码保存为`test.py`，通过下面的命令就可以解析

```bash
adb exec-out screenrecord --output-format=h264 - | python test.py
```

打开 test.jpg 就可能看到一张完美的截图了。

如果手机上没有 screenrecord 这个程序，也可以通过 scrcpy 来代替。这里就暂时不写了。

# 参考

- adb screenrecord + ffmpeg、pyav 相关代码参考 [https://github.com/PyAV-Org/PyAV/issues/578](https://github.com/PyAV-Org/PyAV/issues/578)
- [https://pyav.org/docs/develop/api/video.html#av.video.frame.VideoFrame](https://pyav.org/docs/develop/api/video.html#av.video.frame.VideoFrame)
