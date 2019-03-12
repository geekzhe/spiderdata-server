# spiderdata-server

## 简介

spiderdata-server 为 spiderdata 项目服务端。

主要模块

* 用户管理
* 数据收集、分析

## 目录结构

```
.
├── README.md
├── setup.py	<--- setuptools 配置文件(定义版本号、依赖库等)
└── spiderdata_server	<--- 项目代码目录(所有代码均放在该目录下)
    ├── cmd		<--- 可执行脚本目录(服务器动脚本等)
    │   └── __init__.py
    ├── db		<--- 数据库操作相关代码目录
    │   ├── __init__.py
    │   ├── mongodb_client.py
    │   └── mysql_client.py
    ├── etc		<--- 配置文件目录
    │   └── spiderdata-server.py	<--- 与环境有关的配置都放到配置文件中(如数据库连接信息、服务器监听地址等)
    ├── __init__.py
    └── server	<--- 具体模块目录
        ├── data	<--- 数据收集、分析功能模块
        │   ├── api.py		<--- API 相关代码(注意，该文件中不涉及具体功能逻辑代码)
        │   ├── __init__.py
        │   └── manager.py		<--- 具体逻辑功能代码
        ├── __init__.py
        └── user	<--- 用户管理功能模块
            ├── api.py
            ├── __init__.py
            └── manager.py
```
