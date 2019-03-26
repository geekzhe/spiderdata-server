# 一对一聊天模块 API 文档

一对一聊天功能基于 WebSocket 实现，API 连接时使用 WebSocket 协议，而不是 HTTP 协议。

## API

> ```<dest_user>``` 为聊天的目标用户
>
> ```<token>``` 为当前登录用户的token

```
/v1/chat/<dest_user>?token=<token>
```

## 连接示例

> JS 中使用下面示例中的方法连接及交互

```
if ("WebSocket" in window) {
    /*
        与服务器建立 websocket 链接
    */
    var ws = new WebSocket("ws://127.0.0.1:7071/v1/chat/tom?token=296d9235-bc89-4566-b8e4-c338e13e0fd7");

	// 处理连接建立时的任务
	ws.onopen = function() {
    	console.log('已连接到服务器！');
		// 其它任务
    };

	// 处理消息发送按钮的点击事件
	sendbtn.onclick = function(event) {
		// 获取输入框里的内容
		var msg = inputArea.value;

		// 组织发送的消息
		var sendMsg = {
			'msg': msg
		}
		
		// 将消息发送给服务器
		ws.send(JSON.stringify(sendMsg));
	}

	// 处理接收到服务器端发送的数据时的任务
    ws.onmessage = function(event) {
		// 打印接收到的数据(JSON格式)，具体数据格式见后文
		console.log(JSON.parse(event.data));
		// 其它任务
	};

	// 处理断开连接时的任务
	ws.onclose = function(event) {
		console.log('与服务器连接已断开！');
		// 其它任务
	}

} else {
    alert('您的浏览器不支持 WebSocket！');
}
```

## 发送数据格式

```
|键|数据类型|功能|
|----|----|----|
|msg|str|存放要发送给对端用户的消息|

{
	'msg': msg
}
```

## 接收数据格式

* 格式

```
{
    'status': 30001,
    'msg': 'OK',
    'body': {
        ...
    }
}
```

```
|键|数据类型|功能|
|----|----|----|
|status|int|标记消息类型|
|msg|str|消息描述信息|
|body|str|消息内容|
```

### 消息类型

|status|消息类型|
|----|----|
|30001|普通聊天消息|
|30002|token验证失败|
|30003|对端用户不存在|
|30098|对端用户上线通知|
|30099|对端用户离线通知|

### 消息示例

* 普通消息(30001)

|键|数据类型|功能|
|----|----|----|
|msg|str|对端用户发送的消息|
|from_user|str|对端用户名|
|send_time|str|(对端)消息发送时间|

```
{
    'status': 30001,
    'msg': 'OK',
    'body': {
        'msg': 'Hello Tom',
        'from_user': 'Jack',
        'send_time': '2019-01-02 11:23:41'
    }
}
```

* token验证失败(30002)

```
{
    'status': 30002,
    'msg': 'Token authentication failed',
    'body': {}
}
```

* 对端用户不存在(30003)

```
{
    'status': 30003,
    'msg': 'Target user Tony does not exist',
    'body': {}
}
```

* 对端用户上线通知(30098)

```
{
    'status': 30098,
    'msg': 'Target user Tom login',
    'body': {}
}
```

* 对端用户离线通知(30099)

```
{
    'status': 30099,
    'msg': 'Target user Tom logout',
    'body': {}
}
```
