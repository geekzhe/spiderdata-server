# 用户模块数据库设计

## 数据库表

### chat_messages

存放用户聊天信息

|字段|数据类型|约束|
|----|----|----|
|uuid|varchar(64)|primary key|
|create_time|varchar(64)|not null|
|update_time|varchar(64)||
|src_user|varchar(64)|not null|
|dest_user|varchar(64)|not null|
|content|text|not null|
|recv_time|varchar(64)|not null|
|has_send|enum('0','1')|default '0' not null|

```
> create table chat_messages (
uuid varchar(64) primary key,
create_time varchar(64) not null,
update_time varchar(64),
src_user varchar(64) not null,
dest_user varchar(64) not null,
content text not null,
recv_time varchar(64) not null,
has_send enum('0','1') default '0' not null
) default charset=utf8;
```
