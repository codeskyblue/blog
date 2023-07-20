---
title: Python peewee时区处理
urlname: mzhvsktyzg76s94q
date: '2023-06-27 15:29:00 +0800'
tags: []
categories: []
toc: true
---

# 背景

MYSQL 中存储的 DATETIME 数据是不包含时区的，这就需要自己来约定一个时区，最好是跟 MYSQL 的配置一致，不然麻烦多多，数据库默认是 CST 也就是+8 时区
数据库字段如果设置了 `DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP`，默认插入的时间就是用的 mysql 时区
peewee 中的时间字段是 DateTimeField

```python
class Base(flask_db.Model):
    id = IntegerField(primary_key=True)
    gmt_create = DateTimeField(default=datetime.now)
    gmt_modified = DateTimeField(default=datetime.now)
```

插入一个数据试试，查数据库看看（接近中午搞的，存储的是北京时间）时间差不多
![](/images/yuque/FuOxfg0z7puANojM7nzIq47XMcgn.png)

```bash
# 进入 mysql：
mysql -u root -p
# 查看当前时区
mysql> show variables like '%time_zone%';
# 设置为北京时间：
mysql> set time_zone='+8:00';
mysql> Query OK, 0 rows affected (0.00 sec)
# 通过 select now () 来验证时区：
mysql> select now();
```

# Peewee 读数据库

我们在看 peewee 读到的数据，全部都变成了 UTC 的时间，这个显然是不对的。
![](/images/yuque/FnrXNVOHHCj09JdtNFP270k5oEHG.png)
谷歌一下也没看到太好的办法，没办法自己定义一个 DateTimeTzField 吧，在代码里面修正一下时区

```python
#
# pip install python-dateutil

from datetime import datetime
from dateutil import tz

# 这里没有用pytz，因为pytz修改时区是多出来6分钟，说是因为用的绝对地点的时差
# 这里用的是python-dateutil，据说说官方开发的。反正挺好用的
CHINA_TZ = tz.gettz("Asia/Shanghai")

class DateTimeTzField(Field):
    field_type = 'DATETIME'

    def db_value(self, value: datetime):
        return value.strftime("%Y-%m-%d %H:%M:%S")

    def python_value(self, value: datetime):
        # 因为field_type是DATETIME，所以value是datetime.datetime类型
        if value is None:
            return None
        return value.replace(tzinfo=CHINA_TZ) # 修正时区
```

数据库的定义改为

```python
class Base(flask_db.Model):
    id = IntegerField(primary_key=True)
    gmt_create = DateTimeTzField(default=datetime.now)
    gmt_modified = DateTimeTzField(default=datetime.now)
```

改完之后总算正常了
![](/images/yuque/FjVHoXpeWi9Bd-D6Ivl283POTlKS.png)
