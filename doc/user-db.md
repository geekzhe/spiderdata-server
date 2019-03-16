# 用户模块数据库设计

## 数据库

spiderdata

```
> create database spiderdata charset=utf8;
```

## 数据库表

### user

用户基本信息表，用于存放用户基本信息

|字段|数据类型|约束|
|----|----|----|
|uuid|varchar(64)|primary key|
|create_time|varchar(64)|not null|
|update_time|varchar(64)||
|username|varchar(64)|unique not null|
|password|varchar(128)|not null|
|birthday|varchar(32)||
|email|varchar(64)|unique not null|
|active|enum('0','1')|default '0' not null|

```
> create table user (
uuid varchar(64) primary key,
create_time varchar(64) not null,
update_time varchar(64),
username varchar(64) unique not null,
password varchar(128) not null,
birthday varchar(32),
email varchar(64) unique not null,
active enum('0','1') default '0' not null
) default charset=utf8;
```

### user_work_info

用户工作信息表，用于存放与工作有关的信息

|字段|数据类型|约束|
|----|----|----|
|uuid|varchar(64)|primary key|
|create_time|varchar(64)|not null|
|update_time|varchar(64)||
|user_uuid|varchar(64)|unique not null|
|work_start|varchar(32)||
|education|enum('小学','初中','高中','大专','本科','硕士','博士')||
|work_city|varchar(32)||

```
> create table user_work_info (
uuid varchar(64) primary key,
create_time varchar(64) not null,
update_time varchar(64),
user_uuid varchar(64) unique not null,
work_start varchar(32),
education enum('小学','初中','高中',' 大专','本科','硕士','博士'),
work_city varchar(32)
) default charset=utf8;
```

### user_skill

用户技能信息表，用于存放用户技能信息

|字段|数据类型|约束|
|----|----|----|
|uuid|varchar(64)|primary key|
|create_time|varchar(64)|not null|
|update_time|varchar(64)||
|user_uuid|varchar(64)|unique not null|
|skills|text||

```
> create table user_skill (
uuid varchar(64) primary key,
create_time varchar(64) not null,
update_time varchar(64),
user_uuid varchar(64) unique not null,
skills text
) default charset=utf8;
```

### user_messages

用户消息(站内信)表，用于存放用户消息

|字段|数据类型|约束|
|----|----|----|
|id|int(128)|primary key auto_increment|
|create_time|varchar(64)|not null|
|update_time|varchar(64)||
|user_uuid|varchar(64)|not null|
|title|varchar(256)|not null|
|content|text||
|has_read|enum('0','1')|default '0' not null|
|deleted|enum('0','1')|default '0' not null|

```
> create table user_messages (
id int primary key auto_increment,
create_time varchar(64) not null,
update_time varchar(64),
user_uuid varchar(64) not null,
title varchar(256) not null,
content text,
has_read enum('0','1') default '0' not null,
deleted enum('0','1') default '0' not null
) default charset=utf8;
```

### user_tokens

用户 token 表，用于存放用户 token

|字段|数据类型|约束|
|----|----|----|
|token|varchar(64)|unique not null|
|expire|varchar(64)|not null|
|deleted|enum('0','1')|default '0' not null|

```
create table user_tokens (
token varchar(64) unique not null,
expire varchar(64) not null,
deleted enum('0','1') default '0' not null
) default charset=utf8;
```
