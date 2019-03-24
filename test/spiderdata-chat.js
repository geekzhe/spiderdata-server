/*
    从页面获取操作对象
*/
// 显示对端用户名区域
var peer_user = document.querySelector('#peer_user_name');
// 显示对端用户在线状态区域
var user_online = document.querySelector('#peer_user_online');

// 消息展示框
var msgs = document.querySelector('#messages');

// 消息展示框显示消息时间间隔时间  时间 = 分钟 * 秒 * 毫秒
var showTimeInterval = 1 * 60 * 1000;
// var showTimeInterval = 5 * 1000;

// 显示消息时间标记
var showTimeFlag = true;

// 消息发送间隔计时器ID
var showTimeTimerID = 0;

// 记录上一条消息的发送实现
var lastMsgSendTime = null;

// 输入框
var input_area = document.querySelector('#input_area');
// 发送按钮
var sendbtn = document.querySelector('#submit');

// 定义保存错误信息的对象
var errorData = {};

/*
    WebSocket 服务器链接信息
*/
var server_ip = '127.0.0.1';
var server_port = 7071;
var server_api = '/v1/chat';

/*
    聊天目标用户及当前用户token
*/
var p_user = localStorage.getItem('p_user');
var token = localStorage.getItem('token');

function generateNotifyMsg(title, msgs) {
    // var tempPrefix = '<div class="error_dialog"><span>错误！</span><br>';
    var tempPrefix = '<div class="error_dialog">';
    var title = '<span><b>' + title + '</b></span><br>';
    var tempSuffix = '</div>';
    var content = '';
    for (i in msgs) {
        content += ('<span>' + msgs[i] + '</span><br>');
    }
    var errorMsg = tempPrefix + title + content + tempSuffix;
    return errorMsg
}

function showMsgTime(time) {
    var temPrefix = '<div class="showTime"><span>';
    var temSuffix = '</span></div>';
    var msgTime = temPrefix + time + temSuffix;

    return msgTime
}

function resetShowTimeTimer() {
    // 关闭旧的计时器
    if (showTimeTimerID) {
        clearTimeout(showTimeTimerID);
    }

    // 设置新的计时器
    showTimeTimerID = setTimeout(function () {
        showTimeFlag = true;
    }, showTimeInterval);
}

function getCurrentDateTime() {
    var dt = new Date();
    var year = dt.getFullYear();
    var month = (dt.getMonth() + 1) < 10 ? '0' + (dt.getMonth() + 1) : dt.getMonth();
    var day = dt.getDate() < 10 ? '0' + dt.getDate() : dt.getDate();
    var currentDate = [year, month, day].join('-');
    var currentTime = dt.toLocaleTimeString('zh-CN', {hour12: false});
    var currentDateTime = [currentDate, currentTime].join(' ')
    return currentDateTime
}

/*
    返回两个时间点之间的间隔(单位:ms)
 */
function getTimeInterval(t1, t2) {
    var d1 = new Date(t1);
    var d2 = new Date(t2);
    // var interval = Math.abs(((d2 - d1)/1000/60).toFixed(0));
    var interval = Math.abs(d1 - d2);

    return interval
}

if ("WebSocket" in window) {
    /*
        与服务器建立 websocket 链接
    */
    // 格式：ws://服务器IP:服务器端口/v1/chat/目标用户名?token=当前用户token
    var ws = new WebSocket("ws://" + server_ip + ":" + server_port +
        server_api + "/" + p_user + "?token=" + token);

    /*
        连接建立成功时要做的处理
    */
    ws.onopen = function() {
        console.log('已连接上！');
        peer_user.innerHTML = '正在与 ' + p_user + ' 聊天';
        user_online.innerHTML = '对方 离线';
    };

    /*
        处理页面发送按钮提交事件(发送消息)
    */
    sendbtn.onclick = function (e) {
        // 获取输入框里的内容
        var right_msg = input_area.value;
        if (!right_msg) return;

        // 显示消息发送时间
        var current_time = getCurrentDateTime();
        if (lastMsgSendTime && getTimeInterval(lastMsgSendTime, current_time) > showTimeInterval) {
            showTimeFlag = true;
        }
        if (showTimeFlag) {
            msgs.innerHTML = msgs.innerHTML + showMsgTime(current_time);
            showTimeFlag = false;
            lastMsgSendTime = current_time;
        }
        resetShowTimeTimer();

        // 将用户输入的消息显示在消息框中
        var right = '<div class="righttalk"><span>' + right_msg + '</span></div>';
        msgs.innerHTML = msgs.innerHTML + right;
        msgs.scrollTop = msgs.scrollHeight;
        input_area.value = '';

        // 发送消息
        var send_msg = {
            'msg': right_msg
        };
        ws.send(JSON.stringify(send_msg));
    };
    // 处理输入框中的回车事件，回车时触发发送按钮的点击事件
    input_area.onkeydown = function (e) {
        if (e.code == 'Enter') {
            sendbtn.click();
        };
    };

    /*
        收到消息时要做的处理(将消息显示在页面上)
    */
    ws.onmessage = function(event) {
        var data = JSON.parse(event.data);
        /*
        data 数据格式
        {
            'status': 30001,
            'msg': 'OK',
            'body': {
                'msg': '用户发送的消息',
                'from_user': '消息发送者',
                'send_time': '消息发送时间'
            }
        }
        */
        if (data['status'] == '30001') {
            // 当接收到的数据状态为 30001 时，为正常用户消息，提取消息进行展示
            // 注意：用户消息为 data['body']['msg'] 而不是 data['msg']

            // 显示消息发送时间
            var msg_time = data['body']['send_time'];
            if (showTimeFlag) {
                msgs.innerHTML = msgs.innerHTML + showMsgTime(msg_time);
                showTimeFlag = false;
                lastMsgSendTime = msg_time;
            }
            if (lastMsgSendTime && getTimeInterval(lastMsgSendTime, msg_time) > showTimeInterval) {
                showTimeFlag = true;
            }
            resetShowTimeTimer();

            // 将消息显示在消息框中(靠右侧显示)
            var left_msg = data['body']['msg'];
            var left = '<div class="lefttalk"><span>' + left_msg + '</span></div>';
            msgs.innerHTML = msgs.innerHTML + left;
            msgs.scrollTop = msgs.scrollHeight;

            // 控制台打印消息
            // console.log(data['body']['msg']);
        } else if (data['status'] == '30098') {
            // 对端用户上线
            user_online.innerHTML = '对方 在线';
            peer_user.innerHTML = '正在与 ' + p_user + ' 聊天';
        } else if (data['status'] == '30099') {
            // 对端用户离线
            user_online.innerHTML = '对方 离线';
            peer_user.innerHTML = '正在与 ' + p_user + ' 聊天';
        } else {
            // 数据状态为其它状态时，为其它消息，根据状态码对应的不同的事件分别处理
            errorData = data;
        }
    };

    /*
        处理连接断开事件
    */
    ws.onclose = function(event) {
        console.log('与服务器连接已断开！');
        var errorMsgs = [];
        if (errorData) {
            console.log(errorData);
            errorMsgs = [
                // errorData['msg'] ? errorData != undefined : '请刷新重试',
                // 'Code: ' + (errorData['status'] ? errorData : 300090),
                 errorData['msg'] != undefined ? errorData['msg'] :
                     '请刷新重试',
                'Code: ' + (errorData['status'] !== undefined ?
                    errorData['status'] : 300090),
            ];
        }
        msgs.innerHTML = msgs.innerHTML + generateNotifyMsg('服务器连接已断开', errorMsgs);
        // 禁用控件
        input_area.disabled = true;
        sendbtn.disabled = true;
        msgs.classList.add('lock');
        // 更新状态提示信息
        peer_user.innerHTML = '未连接';
        user_online.innerHTML = '未连接';
    }
} else {
    alert('您的浏览器不支持 WebSocket！');
}