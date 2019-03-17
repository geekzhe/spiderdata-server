# spiderdata-server

## 简介

spiderdata-server 为 spiderdata 项目服务端。

主要模块

* 用户管理
* 数据收集、分析

## 安装方法

* 下载代码到本地

```
$ git clone https://github.com/spiderdata/spiderdata-server.git
```

* 切换工作目录

```
$ cd spiderdata-server
```

* 将 spiderdata-server 安装到系统中

```
$ sudo python3 setup.py install
```

## 使用方法

* 创建名为 spiderdata 的数据库

```
mysql> create database spiderdata charset=utf8;
```

* 导入数据库表结构

> 注意：以下命令中数据库的 IP、用户名根据自己的环境配置进行填写

```
mysql -uroot -h 127.0.0.1 spiderdata -p < spiderdata.sql
```

* 修改配置文件

> 重要！！！
>
> 根据自己环境的情况修改对应配置

```
$ vim spiderdata_server/etc/settings.py
# Mysql 连接配置                                                                
                                                                                
MYSQL_HOST = '127.0.0.1'                                                        
MYSQL_PORT = 3306                                                               
MYSQL_USERNAME = 'root'                                                         
MYSQL_PASSWORD = '123456'                                                       
MYSQL_DATABASE_NAME = 'spiderdata'                                              
                                                                                
# MongoDB 连接配置                                                              
                                                                                
                                                                                
# 用户服务相关配置                                                              
                                                                                
USER_API_HOST = '0.0.0.0'                                                       
USER_API_PORT = 7070
```

* 启动服务器

```
$ python3 spiderdata_server/cmd/run_user_api.py
 * Serving Flask app "spiderdata_server.server.user.api" (lazy loading)
 * Environment: production
   WARNING: Do not use the development server in a production environment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://0.0.0.0:7070/ (Press CTRL+C to quit)
```

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
