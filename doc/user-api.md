# 用户模块 API 文档

## 用户注册

* API

```
/v1/user
```

* HTTP 请求方法

```
POST
```

* 请求头

```
Content-Type: application/json
```

* 请求参数

|参数|数据类型|功能|
|----|----|----|
|username|str|用户名|
|password|str|用户密码|
|email|str|用户邮箱|

> 示例

```
{
	"username": "Jerry",
	"password": "happy123",
	"email": "jerry@gmail.com"
}
```

* 响应数据

|参数|数据类型|功能|
|----|----|----|
|status|int|状态码|
|msg|str|描述信息|
|body|dict|返回数据|

|参数|数据类型|功能|
|----|----|----|
|username|str|用户名|

> 示例

```
{
    "body": {
        "username": "Jerry"
    },
    "msg": "Registration success",
    "status": 10001
}
```


## 用户登陆

* API

```
/v1/user/token
```

* HTTP 请求方法

```
POST
```

* 请求头

```
Content-Type: application/json
```

* 请求参数

|参数|数据类型|功能|
|----|----|----|
|username|str|用户名|
|password|str|用户密码|

> 示例

```

{
	"username": "Jerry",
	"password": "happy123"
}
```

* 响应数据

|参数|数据类型|功能|
|----|----|----|
|status|int|状态码|
|msg|str|描述信息|
|body|dict|返回数据|

|参数|数据类型|功能|
|----|----|----|
|token|str|用户token|
|expire|str|token过期时间|

> 示例

```
{
    "body": {
        "token": "3dac945a-5151-431f-845d-c1bf57a8038e",
		"expire": "2019-01-30 03:20:51"
    },
    "msg": "Login success",
    "status": 10001
}
```

## 用户退出登陆

* API

```
/v1/user/token
```

* HTTP 请求方法

```
DELETE
```

* 请求头

> 注意：<token> 需要替换为登陆时获取到的token

```
Content-Type: application/json
Authorization: Token <token>
```

* 请求参数

|参数|数据类型|功能|
|----|----|----|
|token|str|用户token|

> 示例

```
{
	"token": "3dac945a-5151-431f-845d-c1bf57a8038e"
}
```

* 响应数据

|参数|数据类型|功能|
|----|----|----|
|status|int|状态码|
|msg|str|描述信息|
|body|dict|返回数据(空字典)|

> 示例

```
{
    "body": {},
    "msg": "Logout success",
    "status": 10001
}
```

## 获取用户信息

* API

```
/v1/user/profile
```

* HTTP 请求方法

```
GET
```

* 请求头

> 注意：<token> 需要替换为登陆时获取到的token

```
Content-Type: application/json
Authorization: Token <token>
```

* 请求参数

无

* 响应数据

|参数|数据类型|功能|
|----|----|----|
|status|int|状态码|
|msg|str|描述信息|
|body|dict|返回数据|

|参数|数据类型|功能|
|----|----|----|
|username|str|用户名|
|email|str|邮箱|
|birthday|str|生日(YYYY-MM-DD)|
|working_start|str|参加工作时间(YYYY-MM-DD HH:MM:SS)|
|education|str|学历|
|city|str|所在城市|

> 示例

```
{
    "body": {
		"username": "Jerry",
		"email": "jerry@gmail.com",
		"birthday": "1993年08月23日",
		"working_start": "2015年7月",
		"education": "本科"
	},
    "msg": "success",
    "status": 10001
}
```

## 更新用户信息

* API

```
/v1/user/profile
```

* HTTP 请求方法

```
PUT
```

* 请求头

> 注意：<token> 需要替换为登陆时获取到的token

```
Content-Type: application/json
Authorization: Token <token>
```

* 请求参数

> 请求参数为要修改的内容，例如修改学历

|参数|数据类型|功能|
|----|----|----|
|education|str|修改学历|

> 示例

```
{
	"education": "硕士"
}
```

* 响应数据

|参数|数据类型|功能|
|----|----|----|
|status|int|状态码|
|msg|str|描述信息|
|body|dict|返回数据|

|参数|数据类型|功能|
|----|----|----|
|username|str|用户名|
|email|str|邮箱|
|birthday|str|生日(YYYY-MM-DD)|
|working_start|str|开始工作时间(YYYY-MM-DD HH:MM:SS)|
|education|str|学历|
|city|str|所在城市|

> 示例

```
{
    "body": {
		"username": "Jerry",
		"email": "jerry@gmail.com",
		"birthday": "YYYY-MM-DD",
		"working_start": "YYYY-MM-DD HH:MM:SS",
		"education": "本科"
	},
    "msg": "success",
    "status": 10001
}
```

## 获取用户技能信息

* API

```
/v1/user/skill
```

* HTTP 请求方法

```
GET
```

* 请求头

> 注意：<token> 需要替换为登陆时获取到的token

```
Content-Type: application/json
Authorization: Token <token>
```

* 请求参数

无

* 响应数据

|参数|数据类型|功能|
|----|----|----|
|status|int|状态码|
|msg|str|描述信息|
|body|dict|返回数据|

|参数|数据类型|功能|
|----|----|----|
|skill|list|用户技能列表|

> 示例

```
{
    "body": {
		"skill": [
			"Python",
			"Mysql",
			"Flask",
			"MongoDB",
			"Shell",
			"Redis",
			"Django",
			"Linux",
			"RabbitMQ"
		]
	},
    "msg": "success",
    "status": 10001
}
```

## 修改用户技能信息

* API

```
/v1/user/skill
```

* HTTP 请求方法

```
PUT
```

* 请求头

> 注意：<token> 需要替换为登陆时获取到的token

```
Content-Type: application/json
Authorization: Token <token>
```

* 请求参数

|参数|数据类型|功能|
|----|----|----|
|skill|list|更新后的用户技能列表|

> 示例

```
{
	"skill": [
		"Python",
		"Mysql",
		"Flask",
		"MongoDB",
		"Shell",
		"Redis",
		"Django",
		"Linux",
		"RabbitMQ",
		"HTML",
		"CSS",
		"JS"
	]
}
```

* 响应数据

|参数|数据类型|功能|
|----|----|----|
|status|int|状态码|
|msg|str|描述信息|
|body|dict|返回数据|

|参数|数据类型|功能|
|----|----|----|
|skill|list|用户技能列表|

> 示例

```
{
    "body": {
		"skill": [
			"Python",
			"Mysql",
			"Flask",
			"MongoDB",
			"Shell",
			"Redis",
			"Django",
			"Linux",
			"RabbitMQ",
			"HTML",
			"CSS",
			"JS"
		]
	},
    "msg": "success",
    "status": 10001
}
```

## 获取用户消息(站内信)

* API

```
/v1/user/messages
```

* HTTP 请求方法

```
GET
```

* 请求头

> 注意：<token> 需要替换为登陆时获取到的token

```
Content-Type: application/json
Authorization: Token <token>
```

* 请求参数

|参数|数据类型|功能|
|----|----|----|
|limit|int|单页条目数|
|page|int|页数|

> 示例

```
{
	"limit": 20,
	"page":2
}
```

* 响应数据

|参数|数据类型|功能|
|----|----|----|
|status|int|状态码|
|msg|str|描述信息|
|body|dict|返回数据|

|参数|数据类型|功能|
|----|----|----|
|messages|list|用户消息列表|


|参数|数据类型|功能|
|----|----|----|
|id|int|消息ID|
|title|str|消息标题|
|content|str|消息内容|
|read|bool|阅读状态(True:已读;False:未读)|

> 示例

```
{
	"body":{
		"messages":[
			{
				"id": 1,
				"title": "系统通知",
				"content": "本周行业趋势分析报告已经发送到您的邮箱，请注意查收。",
				"read": False
			},
			{
				"id": 2,
				"title": "您有来自 Tom 的新消息",
				"content": ""
				"read": False
			}
		]
	},
    "msg": "success",
    "status": 10001
}
```

## 更新用户消息(站内信)状态

更新消息状态为已读

* API

```
/v1/user/messages
```

* HTTP 请求方法

```
PUT
```

* 请求头

> 注意：<token> 需要替换为登陆时获取到的token

```
Content-Type: application/json
Authorization: Token <token>
```

* 请求参数

|参数|数据类型|功能|
|----|----|----|
|id|int|要更新为已读状态的消息的ID|

> 示例

```
{
	"id": 1
}
```

* 响应数据

|参数|数据类型|功能|
|----|----|----|
|status|int|状态码|
|msg|str|描述信息|
|body|dict|返回数据(无)|

> 示例

```
{
    "body": {},
	"msg": "success",
	"status": 10001
}
```

## 删除用户消息(站内信)

删除用户消息(站内信)

* API

```
/v1/user/messages
```

* HTTP 请求方法

```
DELETE
```

* 请求头

> 注意：<token> 需要替换为登陆时获取到的token

```
Content-Type: application/json
Authorization: Token <token>
```

* 请求参数

|参数|数据类型|功能|
|----|----|----|
|id|int|要删除的消息的ID|

> 示例

```
{
	"id": 1
}
```

* 响应数据

|参数|数据类型|功能|
|----|----|----|
|status|int|状态码|
|msg|str|描述信息|
|body|dict|返回数据(无)|

> 示例

```
{
    "body": {},
	"msg": "success",
	"status": 10001
}
```

## 账号激活

通过邮箱中的激活链接激活账号

* API

```
/v1/user/account_activation/<activation_code>
```

* HTTP 请求方法

```
GET
```

* 请求头

```
Content-Type: application/json
```

* 请求参数

无

* 响应数据

|参数|数据类型|功能|
|----|----|----|
|status|int|状态码|
|msg|str|描述信息|
|body|dict|返回数据(无)|

> 示例

```
{
	"body": {},
	"msg": "success",
	"status": 10001
}
```

