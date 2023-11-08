---
title: Flask Prometheus监控
urlname: flask_prometheus_grafana
date: '2023-05-17 17:40:18 +0800'
tags:
  - flask
  - prometheus
categories: []
toc: true
---

# 简介

就算是在稳定的应用也有一天会崩掉，而且如果一个服务不被监控就很难保证其稳定性。本文介绍了如何使用使用业界最流行的 Prometheus、Grafana 来实现 Flask 应用的监控

- 应用程序通过 HTTP /metrics 透出数据
- Prometheus 根据配置文件 prometheus.yml 中获取到的应用节点定时拉数据
- Grafana 负责做前端展示
- Alertmanager 负责做通知

其中 Prometheus 由前谷歌工程师在 Soundcloud 上以开源软件的形式进行研发。2012 年创立，目前已经发展到了 2.0
![](/images/yuque/FlncHFwJk32uIHd0BIN1dNsL3c2n.png)

# Flask 应用配置

一般 Flask 的部署基本上都是 Gunicorn，这里就不讲别的方案了

1. 代码修改

app.py 文件中修改为下面的内容

```python
import flask
from prometheus_flask_exporter.multiprocess import GunicornInternalPrometheusMetrics

app = flask.Flask(__name__)
# 重要是下面这两行
metrics = GunicornInternalPrometheusMetrics(app)
metrics.info('app_info', 'Application info', version='0.1.0')

@app.route("/ruok")
def ruok():
    return "imok"
```

添加 python 库 prometheus_flask_exporter 到 requirements.txt 中

2. 运行脚本修改

因为 gunicorn 会有多个 worker，为了在多进程环境下通过/metrics 获取到的数据是一致的，需要将数据保存在本地共享

```bash
#!/bin/bash -ex
#

export PROMETHEUS_MULTIPROC_DIR=$PWD/tmp/prometheus
mkdir -p "$PROMETHEUS_MULTIPROC_DIR"

gunicorn -b 0.0.0.0:7001 -w 2 app:app
```

3. 测试

```bash
$curl localhost:7001/ruok # 接口请求一下
imok
$curl localhost:7001/metrics # 查询统计到的数据
# 在请求的最后应该可以看到一句
flask_http_request_total{method="GET",status="200"} 1.0
```

# Prometheus 和 Grafana 安装

就写 Docker 的使用方式吧，比较比较方便

```yaml
version: "3"

volumes:
  prometheus-data:
    driver: local
  grafana-data:
    driver: local

services:
  prometheus:
    image: prom/prometheus:latest
    container_name: prometheus
    ports:
      - "9090:9090"
    volumes:
      - /etc/prometheus:/etc/prometheus
      - prometheus-data:/prometheus
    restart: unless-stopped
    command:
      - "--config.file=/etc/prometheus/prometheus.yml"

  grafana:
    image: grafana/grafana:latest
    container_name: grafana
    ports:
      - "3000:3000"
    volumes:
      - grafana-data:/var/lib/grafana
    restart: unless-stopped

  # 下面这个可选，加上的话需要在prometheus.yml中同步修改
  node_exporter:
    image: quay.io/prometheus/node-exporter:latest
    container_name: node_exporter
    command:
      - "--path.rootfs=/host"
    pid: host
    restart: unless-stopped
    volumes:
      - "/:/host:ro,rslave"
```

准备一下 prometheus 的配置文件

```yaml
global:
  scrape_interval: 15s # By default, scrape targets every 15 seconds.

  # Attach these labels to any time series or alerts when communicating with
  # external systems (federation, remote storage, Alertmanager).
  # external_labels:
  #  monitor: 'codelab-monitor'

# A scrape configuration containing exactly one endpoint to scrape:
# Here it's Prometheus itself.
scrape_configs:
  # The job name is added as a label `job=<job_name>` to any timeseries scraped from this config.
  - job_name: "prometheus"
    # Override the global default and scrape targets from this job every 5 seconds.
    scrape_interval: 5s
    static_configs:
      - targets: ["localhost:9090"]
```

先写到这里吧，等我配置完，再继续写

# 参考

- [https://github.com/rycus86/prometheus_flask_exporter](https://github.com/rycus86/prometheus_flask_exporter)
- Prometheus 官网 [https://prometheus.io/](https://prometheus.io/)
- [https://dev.to/chinhh/server-monitoring-with-prometheus-and-grafana-266o](https://dev.to/chinhh/server-monitoring-with-prometheus-and-grafana-266o)
- 这个写的很全 [https://yunlzheng.gitbook.io/prometheus-book/](https://yunlzheng.gitbook.io/prometheus-book/)
