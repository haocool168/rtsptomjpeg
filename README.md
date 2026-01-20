# RtspTomJpeg

## 前言

本项目的初衷为用esp8266+点灯科技blinker 开发的远程门锁与门口监控画面整合blinkerApp中 .

了将你的 MJPEG 视频流服务（基于 Flask + OpenCV 读取 RTSP）打包为 Docker 镜像，以下是完整的步骤，包括容错重连机制

------

## 构建  Docker 镜像

- 下载拉取 我的是ubuntu系统
- 修改mjpeg_stream.py中的 **RTSP_URL**参数， 为rtsp地址，我的是Tplink的摄像头。
- rtsp://用户名:密码@ip:554/stream2（其它品牌可自行查询）

如：

```python
rtsp_url = "rtsp://admin:admin@192.168.31.99:554/stream2"
```

- 构建镜像

```shell
docker build -t rtsp-mjpeg-stream .
```



## 如何部署docker

```shell
docker run -d -p 5589:5589 --name mjpeg-server rtsp-mjpeg-stream
```

## 访问方式

打开浏览器访问：

http://<服务器IP>:5589/video_feed



